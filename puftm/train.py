'''
puftm :: train (CLI)
'''
import os
import argparse
import random
import numpy as np
import torch as th
from . import lenet
from . import datasets
from . import engine
import rich
console = rich.get_console()


def main():
    ag = argparse.ArgumentParser('Train a neural network!')
    # datasets
    ag.add_argument('--dataset', '-d', type=str, required=True,
            choices=('mnist',))
    # models
    ag.add_argument('--model', '-m', type=str, required=True,
            choices=('lenet',))
    ag.add_argument('--resume', '-r', type=str, default=None)
    # optimizers
    ag.add_argument('--lr', type=float, default=1e-3)
    ag.add_argument('--weight_decay', type=float, default=1e-5)
    ag.add_argument('--lr_drop', type=int, default=12)
    ag.add_argument('--seed', type=int, default=42)
    # training
    ag.add_argument('--epochs', type=int, default=16)
    ag.add_argument('--device', type=str, default='cpu' if
            not th.cuda.is_available() else 'cuda')
    # logging
    ag.add_argument('--logdir', type=str, default='exps/{dataset}_{model}')
    # distributed
    ag.add_argument('--local_rank', type=int, default=None)
    # parse and prepare
    ag = ag.parse_args()
    ag.logdir = ag.logdir.format(dataset=ag.dataset, model=ag.model)
    if not os.path.exists(ag.logdir):
        os.makedirs(ag.logdir)
    if os.getenv('LOCAL_RANK', None) is not None:
        ag.local_rank = int(os.getenv('LOCAL_RANK'))
    th.manual_seed(ag.seed)
    random.seed(ag.seed)
    np.random.seed(ag.seed)
    console.print(ag)
    if ag.local_rank is not None:
        if not th.cuda.is_available():
            raise NotImplementedError('distributed not implemented for cpu')
        th.cuda.set_device(ag.local_rank)
        th.distributed.init_process_group(backend='NCCL', init_method='env://')
    console.print('[bold white on violet]>_< init OK. Start training ...')
    # launch!
    try:
        main_(ag)
    except KeyboardInterrupt:
        if os.getenv('LOCAL_RANK', None) is not None:
            th.distributed.destroy_process_group()
        console.print('[white on red]>_< pulled down processes.')
        exit()


def main_(ag: object):
    # initialize model and optimizer
    model_constructors = {'lenet': lenet.LeNet,}
    model = model_constructors[ag.model]().to(ag.device)
    # resume?
    if ag.resume is not None:
        console.print(f'[white on blue]>_< resuming from state dict {ag.resume}')
        state_dict = th.load(ag.resume, map_location=ag.device)
        model.load_state_dict(state_dict, strict=True)
    # distributed?
    if ag.local_rank is not None:
        model = th.nn.parallel.DistributedDataParallel(model,
                device_ids=[ag.local_rank], output_device=ag.local_rank,
                find_unused_parameters=False)
    optim = th.optim.Adam(model.parameters(),
            lr=ag.lr,
            weight_decay=ag.weight_decay)
    scheduler = th.optim.lr_scheduler.MultiStepLR(optim,
            milestones=[ag.lr_drop], gamma=0.1)
    if ag.local_rank is None or th.distributed.get_rank() == 0:
        console.print(model)
        console.print(f'-- Optimizer:', optim)
        console.print(f'-- Scheduler:', scheduler)

    # dataset loader
    dataset_names = {'mnist': 'MNIST'}
    ltrain = datasets.get_dataset_loader(dataset_names[ag.dataset], 'train')
    ltest = datasets.get_dataset_loader(dataset_names[ag.dataset], 'test')

    # first evaluation
    model.eval()
    engine.evaluate_one_epoch(model, ltest, epoch=-1, device=ag.device,
            logdir=ag.logdir, local_rank=ag.local_rank)

    # start training!
    for epoch in range(ag.epochs):
        # train one epoch
        model.train()
        engine.train_one_epoch(model, optim, ltrain,
                epoch=epoch, device=ag.device, logdir=ag.logdir,
                local_rank=ag.local_rank)
        # evaluate one epoch
        model.eval()
        engine.evaluate_one_epoch(model, ltest,
                epoch=epoch, device=ag.device, logdir=ag.logdir,
                local_rank=ag.local_rank)
        # learning rate scheduler
        scheduler.step()


if __name__ == '__main__':
    main()
