'''
puftm :: evaluate (CLI)
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
    ag = argparse.ArgumentParser('Evaluate a neural network!')
    # datasets
    ag.add_argument('--dataset', '-d', type=str, required=True,
            choices=('mnist',))
    # models
    ag.add_argument('--model', '-m', type=str, required=True,
            choices=('lenet',))
    # evaluation
    ag.add_argument('--resume', '-r', type=str,
            default='{logdir}/model_latest.pt')
    ag.add_argument('--device', type=str, default='cpu' if
            not th.cuda.is_available() else 'cuda')
    # logging
    ag.add_argument('--logdir', type=str, default='exps/{dataset}_{model}')
    # distributed
    ag.add_argument('--local_rank', type=int, default=None)
    # parse and prepare
    ag = ag.parse_args()
    ag.logdir = ag.logdir.format(dataset=ag.dataset, model=ag.model)
    ag.resume = ag.resume.format(logdir=ag.logdir)
    if not os.path.exists(ag.logdir):
        os.makedirs(ag.logdir)
    if os.getenv('LOCAL_RANK', None) is not None:
        ag.local_rank = int(os.getenv('LOCAL_RANK'))
    console.print(ag)
    if ag.local_rank is not None:
        if not th.cuda.is_available():
            raise NotImplementedError('distributed not implemented for cpu')
        th.cuda.set_device(ag.local_rank)
        th.distributed.init_process_group(backend='NCCL', init_method='env://')
    console.print('[bold white on violet]>_< init OK. Start eval ...')
    # launch!
    try:
        main_(ag)
    except KeyboardInterrupt:
        if os.getenv('LOCAL_RANK', None) is not None:
            th.distributed.destroy_process_group()
        console.print('[white on red]>_< pulled down processes.')
        exit()


def main_(ag: object):
    # initialize model and resume 
    model_constructors = {'lenet': lenet.LeNet,}
    model = model_constructors[ag.model]().to(ag.device)
    if ag.local_rank is not None:
        model = th.nn.parallel.DistributedDataParallel(model,
                device_ids=[ag.local_rank], output_device=ag.local_rank,
                find_unused_parameters=False)
    if ag.local_rank is None or th.distributed.get_rank() == 0:
        console.print(model)
    # resume
    console.print(f'>_< loading state dict from {ag.resume}')
    state_dict = th.load(ag.resume, map_location=ag.device)
    if ag.local_rank is not None:
        model.module.load_state_dict(state_dict, strict=True)
    else:
        model.load_state_dict(state_dict, strict=True)

    # dataset loader
    dataset_names = {'mnist': 'MNIST'}
    ltest = datasets.get_dataset_loader(dataset_names[ag.dataset], 'test')

    # run evaluation
    model.eval()
    engine.evaluate_one_epoch(model, ltest, epoch=-1, device=ag.device,
            logdir=ag.logdir, local_rank=ag.local_rank,
            save_state_dict=False)


if __name__ == '__main__':
    main()
