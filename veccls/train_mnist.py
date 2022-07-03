import os
import argparse
import torch as th
import torch.nn.functional as F
from . import mnist_dataset
import rich
from rich.progress import track
from . import recurrent
from . import transformer
from . import engine
console = rich.get_console()


def train_mnist():
    ag = argparse.ArgumentParser('''Train an MNIST model, vector graphics!
    (1) Passing in the color and translate as h0 to RNN slightly improves
        performance, from 95.5 to 95.8 (model_type=gru), only using longest
    ''')
    # -- recurrent neural network and transformer settings --
    ag.add_argument('--model_type', type=str, default='gru',
            choices=('rnn', 'gru', 'lstm',
                'hrnn', 'hgru', 'hlstm', 'pst', 'hpst'))
    ag.add_argument('--input_size', type=int, default=2)
    ag.add_argument('--hidden_size', type=int, default=64)
    ag.add_argument('--num_layers', type=int, default=3)
    ag.add_argument('--nhead', type=int, default=2)
    ag.add_argument('--dropout', type=float, default=0.01)
    # -- optimizer and training setting --
    ag.add_argument('--lr', type=float, default=1e-3)
    ag.add_argument('--weight_decay', type=float, default=1e-7)
    ag.add_argument('--epochs', type=int, default=16)
    ag.add_argument('--lr_drop', type=int, default=12)
    ag.add_argument('--device', type=str, default='cpu'
            if not th.cuda.is_available() else 'cuda')
    # -- logging and file operations --
    ag.add_argument('--logdir', type=str, default='train_mnist_')
    # -- distributed training --
    # https://pytorch.org/docs/stable/distributed.html#launch-utility
    ag.add_argument('--local_rank', type=int, default=None)
    ag = ag.parse_args()
    ag.logdir = ag.logdir + ag.model_type
    console.print(ag)

    if not os.path.exists(ag.logdir):
        os.mkdir(ag.logdir)
    if ag.local_rank is not None:
        if not th.cuda.is_available():
            raise NotImplementedError('distributed not implemented for cpu')
        th.cuda.set_device(ag.local_rank)
        th.distributed.init_process_group(backend='NCCL', init_method='env://')
    else:
        console.print('[bold white on violet]>_< start training MnistRNN')

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
    console.print(model)
    console.print(f'-- Number of parameters:', model.num_params)
    if ag.local_rank is not None:
        model = th.nn.parallel.DistributedDataParallel(model,
                device_ids=[ag.local_rank], output_device=ag.local_rank)
    optim = th.optim.Adam(model.parameters(),
        lr=ag.lr, weight_decay=ag.weight_decay)
    scheduler = th.optim.lr_scheduler.MultiStepLR(optim,
            milestones=[ag.lr_drop], gamma=0.1)
    console.print(f'-- Optimizer:', optim)
    console.print(f'-- Scheduler:', scheduler)

    loadertrn = mnist_dataset.get_mnist_loader(split='train',
            batch_size=128,
            longest=False if ag.model_type.startswith('h') else True)
    loadertst = mnist_dataset.get_mnist_loader(split='test',
            batch_size=100,
            longest=False if ag.model_type.startswith('h') else True)

    # evaluate before train
    model.eval()
    engine.evaluate(model, loadertst,
            epoch=-1, device=ag.device, logdir=ag.logdir)
    for epoch in range(ag.epochs):
        console.print(f'>_< training epoch {epoch} ...')

        # train one epoch
        model.train()
        engine.train_one_epoch(model, optim, loadertrn,
                epoch=epoch, device=ag.device, logdir=ag.logdir)

        # evaluate
        model.eval()
        engine.evaluate(model, loadertst,
                epoch=epoch, device=ag.device, logdir=ag.logdir)

        # adjust learning rate
        scheduler.step()


if __name__ == '__main__':
    train_mnist()
