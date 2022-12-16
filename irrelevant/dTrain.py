#!/usr/bin/env python3
'''
https://zhuanlan.zhihu.com/p/76638962
https://pytorch.org/docs/stable/distributed.html#
https://pytorch.org/tutorials/intermediate/ddp_tutorial.html
https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html
https://zhuanlan.zhihu.com/p/86441879
'''
import sys
import argparse
import os
import torch as th
from termcolor import cprint, colored
import lib
import yaml
from torch.utils.tensorboard import SummaryWriter


def _train_worker(rank, ag:dict={}):
    # initialize the process group
    cprint(f"-- worker[{rank}] | initializing process group ...")
    th.distributed.init_process_group(
            ag.backend, ag.method, rank=rank, world_size=ag.world_size)
    config = yaml.load(open('config.yml', 'r').read(), Loader=yaml.SafeLoader)

    # tensorboard
    if rank == 0:
        writer = SummaryWriter(log_dir='exp0')

    # loading dataset
    cprint(f"-- worker[{rank}] | loading datasets ...")
    trainset = getattr(lib, ag.model).getloader('train', config[ag.model]['batchsize'])
    testset = getattr(lib, ag.model).getloader('test', config[ag.model]['batchsize'])

    # create model and move it to GPU with id rank
    cprint(f"-- worker[{rank}] | initializing models ...")
    model = getattr(lib, ag.model).Model().to(rank)
    model = th.nn.parallel.DistributedDataParallel(model, device_ids=[rank])

    optim = th.optim.SGD(model.parameters(),
            lr=float(config[ag.model]['lr']),
            momentum=float(config[ag.model]['momentum']),
            weight_decay=float(config[ag.model]['weight_decay']))

    if rank == 0:
        valresult = model.module.validate(testset)
        print(colored('Validate[-1] '+str(valresult), 'white', 'on_magenta'))
        writer.add_scalar('Val/loss', valresult.loss, 0)
        writer.add_scalar('Val/accuracy', valresult.accuracy, 0)

    cprint(f"-- worker[{rank}] | start training ...", 'yellow')
    for eph in range(config[ag.model]['epoch']):

        # update learning rate
        lrstep = list(config[ag.model]['lrstep'])
        for (pw, ep) in reversed(list(enumerate(lrstep, 1))):
            if eph >= ep:
                lrn = config[ag.model]['lr'] * (0.1 ** pw)
                for param_group in optim.param_groups:
                    param_group['lr'] = lrn

        # start iterations
        for (i, (im, lb)) in enumerate(trainset):
            model.train()
            im, lb = im.to(rank), lb.to(rank)
            optim.zero_grad()
            outputs = model(im)
            loss = th.nn.functional.cross_entropy(outputs, lb)
            print(f'[Eph w{rank} / {eph}:{i}] loss = {loss.item()}')
            if rank == 0:
                writer.add_scalar('Train/loss', loss.item(), eph * len(trainset) + i)
            loss.backward()
            optim.step()
        if rank == 0:
            valresult = model.module.validate(testset)
            cprint(f'Validate[{eph}] '+str(valresult), 'white', 'on_magenta')
            writer.add_scalar('Val/loss', valresult.loss, eph+1)
            writer.add_scalar('Val/accuracy', valresult.accuracy, eph+1)

    cprint(f"-- worker[{rank}] | pulling down process group ...")
    th.distributed.destroy_process_group()


def Train(argv):
    # arguments
    ag = argparse.ArgumentParser()
    # multi process params
    ag.add_argument('-W', '--world_size', default=th.cuda.device_count())
    ag.add_argument('-B', '--backend', default='nccl')  # fastest
    ag.add_argument('--method', type=str, default='tcp://localhost:40878')
    # Training params
    ag.add_argument('-M', '--model', type=str, default='ct_res18')
    ag = ag.parse_args(argv)
    cprint(ag, 'yellow')
    # spawn workers
    try:
        th.multiprocessing.spawn(
                _train_worker, args=(ag,), nprocs=ag.world_size, join=True)
    except KeyboardInterrupt as e:
        th.distributed.destroy_process_group()
        print(e)


if __name__ == '__main__':
    Train(sys.argv[1:])
