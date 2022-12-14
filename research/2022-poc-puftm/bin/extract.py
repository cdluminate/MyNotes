'''
WIP POC
'''
import sys
sys.path.append('.')
import os
import argparse
import random
import numpy as np
import torch as th
from puftm import lenet
from puftm import datasets
import rich
console = rich.get_console()
from rich.progress import track
from torchvision.models._utils import IntermediateLayerGetter


@th.no_grad()
def extract_one_epoch(model, loader, *,
        epoch, device, logdir, local_rank, save_state_dict,
        dump: str):
    '''
    extract fc2
    '''
    outputs = []
    for (x, y) in track(loader, description='Extract ...'):
        x = x.to(device)
        output = model(x)
        #print(output.shape)
        outputs.append(output.detach().cpu())
    outputs = th.vstack(outputs)
    print(outputs.shape)
    console.print(f'dump extraction to {dump}')
    th.save(outputs, dump)


def main():
    ag = argparse.ArgumentParser('Evaluate a neural network!')
    ag.add_argument('--local_rank', type=int, default=None)
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
    # extraction
    ag.add_argument('--dump', type=str, default='exps/{dataset}_{model}/fc2.pt')
    # parse and prepare
    ag = ag.parse_args()
    ag.logdir = ag.logdir.format(dataset=ag.dataset, model=ag.model)
    ag.dump = ag.dump.format(dataset=ag.dataset, model=ag.model)
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
        raise ValueError  # No dist mode.
    if ag.local_rank is None or th.distributed.get_rank() == 0:
        console.print(model)
    # resume
    console.print(f'>_< loading state dict from {ag.resume}')
    state_dict = th.load(ag.resume, map_location=ag.device)
    model.load_state_dict(state_dict, strict=True)
    # surgery
    model.fc3 = th.nn.Identity()

    # dataset loader
    dataset_names = {'mnist': 'MNIST'}
    ltest = datasets.get_dataset_loader(dataset_names[ag.dataset], 'test')

    # run evaluation
    model.eval()
    extract_one_epoch(model, ltest, epoch=-1, device=ag.device,
            logdir=ag.logdir, local_rank=ag.local_rank,
            save_state_dict=False,
            dump=ag.dump)


if __name__ == '__main__':
    main()
