import os
import argparse
import numpy as np
import random
import torch as th
import torch.nn.functional as F
from . import mnist_dataset
from . import fashion_dataset
from . import cifar10_dataset
import rich
from rich.progress import track
from . import recurrent
from . import transformer
from . import engine
console = rich.get_console()

def main():
    try:
        main_()
    except KeyboardInterrupt:
        if os.getenv('LOCAL_RANK', None) is not None:
            th.distributed.destroy_process_group()
        console.print('[white on red]>_< pulled down processes.')
        exit()

def main_():
    ag = argparse.ArgumentParser('''Train a model for vector graphics!
    (1) Passing in the color and translate as h0 to RNN slightly improves
        performance, from 95.5 to 95.8 (model_type=gru), only using longest
    ''')
    # -- which dataset to use --
    ag.add_argument('--dataset', type=str, required=True,
            choices=('mnist', 'fashion', 'cifar10'))
    # -- recurrent neural network and transformer settings --
    ag.add_argument('--model_type', type=str, default='gru',
            choices=('rnn', 'gru', 'lstm',
                'hrnn', 'hgru', 'hlstm',
                'pst', 'hpst'))
    ag.add_argument('--input_size', type=int, default=2)
    ag.add_argument('--hidden_size', type=int, default=64)
    ag.add_argument('--num_layers', type=int, default=3)
    ag.add_argument('--nhead', type=int, default=8)
    ag.add_argument('--dropout', type=float, default=0.01)
    # -- optimizer and training setting --
    ag.add_argument('--lr', type=float, default=1e-3)
    ag.add_argument('--weight_decay', type=float, default=1e-7)
    ag.add_argument('--batchsize_train', type=int, default=128)
    ag.add_argument('--batchsize_test', type=int, default=100)
    ag.add_argument('--epochs', type=int, default=16)
    ag.add_argument('--lr_drop', type=int, default=12)
    ag.add_argument('--device', type=str, default='cpu'
            if not th.cuda.is_available() else 'cuda')
    # -- logging and miscellaneous --
    ag.add_argument('--logdir', type=str, default='train_{dataset}_{model_type}')
    ag.add_argument('--seed', type=int, default=42)
    # -- distributed training --
    ag.add_argument('--local_rank', type=int, default=None)
    # -- end arguments --
    ag = ag.parse_args()
    # -- post processing --
    ag.logdir = ag.logdir.format(dataset=ag.dataset, model_type=ag.model_type)
    if not os.path.exists(ag.logdir):
        os.mkdir(ag.logdir)
    if os.getenv('LOCAL_RANK', None) is not None:
        ag.local_rank = int(os.getenv('LOCAL_RANK'))
    # https://pytorch.org/docs/stable/notes/randomness.html
    th.manual_seed(ag.seed)
    random.seed(ag.seed)
    np.random.seed(ag.seed)
    # -- done with all argument matter --
    console.print(ag)

    if ag.local_rank is not None:
        # https://pytorch.org/docs/stable/distributed.html#launch-utility
        # https://pytorch.org/tutorials/intermediate/ddp_tutorial.html
        if not th.cuda.is_available():
            raise NotImplementedError('distributed not implemented for cpu')
        th.cuda.set_device(ag.local_rank)
        th.distributed.init_process_group(backend='NCCL', init_method='env://')
    console.print('[bold white on violet]>_< start training ...')

    modelmapping = {
            # only use the longest path. one path per image.
            'rnn': recurrent.LongestPathRNN,
            'gru': recurrent.LongestPathRNN,
            'lstm': recurrent.LongestPathRNN,
            # use all paths. number of paths per image is indefinite.
            'hrnn': recurrent.HierarchicalRNN,
            'hgru': recurrent.HierarchicalRNN,
            'hlstm': recurrent.HierarchicalRNN,
            # only use the longest path
            'pst': transformer.LongestPathTransformer,
            # use all paths
            'hpst': transformer.HierarchicalPathTransformer,
            }
    if ag.model_type in ('rnn', 'gru', 'lstm', 'hrnn', 'hgru', 'hlstm'):
        # is recurrent model
        model = modelmapping[ag.model_type](ag.model_type,
                ag.input_size, ag.hidden_size, ag.num_layers).to(ag.device)
    else:
        # is transformer
        model = modelmapping[ag.model_type](
                model_type=ag.model_type,
                input_size=ag.input_size,
                d_model=ag.hidden_size,
                nhead=ag.nhead,
                d_mlp=ag.hidden_size,
                nlayers=ag.num_layers,
                dropout=ag.dropout).to(ag.device)
    if ag.local_rank is not None:
        model = th.nn.parallel.DistributedDataParallel(model,
                device_ids=[ag.local_rank], output_device=ag.local_rank,
                find_unused_parameters=False)
        model.num_params = model.module.num_params
    optim = th.optim.Adam(model.parameters(),
        lr=ag.lr, weight_decay=ag.weight_decay)
    scheduler = th.optim.lr_scheduler.MultiStepLR(optim,
            milestones=[ag.lr_drop], gamma=0.1)
    if ag.local_rank is None or th.distributed.get_rank() == 0:
        console.print(model)
        console.print(f'-- Number of parameters:', model.num_params)
        console.print(f'-- Optimizer:', optim)
        console.print(f'-- Scheduler:', scheduler)

    dataset_loader = {
            'mnist': mnist_dataset.get_mnist_loader,
            'fashion': fashion_dataset.get_fashion_loader,
            'cifar10': cifar10_dataset.get_cifar10_loader,
            }[ag.dataset]
    loadertrn = dataset_loader(split='train', batch_size=ag.batchsize_train,
            longest=False if ag.model_type.startswith('h') else True)
    loadertst = dataset_loader(split='test', batch_size=ag.batchsize_test,
            longest=False if ag.model_type.startswith('h') else True)

    # evaluate before train
    model.eval()
    engine.evaluate(model, loadertst,
            epoch=-1, device=ag.device, logdir=ag.logdir,
            local_rank=ag.local_rank)
    for epoch in range(ag.epochs):

        # train one epoch
        model.train()
        engine.train_one_epoch(model, optim, loadertrn,
                epoch=epoch, device=ag.device, logdir=ag.logdir,
                local_rank=ag.local_rank)

        # evaluate
        model.eval()
        engine.evaluate(model, loadertst,
                epoch=epoch, device=ag.device, logdir=ag.logdir,
                local_rank=ag.local_rank)

        # adjust learning rate
        scheduler.step()


if __name__ == '__main__':
    main()
