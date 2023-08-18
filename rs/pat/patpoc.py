'''
POC for ParetoAT
'''
import numpy as np
import torch as th
import torchvision as V
from torchvision.models._utils import IntermediateLayerGetter
import argparse
import time
import rich
from collections import defaultdict
from rich.progress import track
console = rich.get_console()

def check_resnet18(args):
    M = getattr(V.models, ag.model)().to(args.device)
    print(M)
    M0p = IntermediateLayerGetter(M, {'maxpool': 'maxpool'})
    M1 = IntermediateLayerGetter(M, {'layer1':'layer1'})
    M2 = IntermediateLayerGetter(M, {'layer2':'layer2'})
    M3 = IntermediateLayerGetter(M, {'layer3':'layer3'})
    M4 = IntermediateLayerGetter(M, {'layer4':'layer4'})
    Tforward = defaultdict(list)
    Tbackward = defaultdict(list)
    for i in track(range(args.maxiter)):
        x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True

        def _get_forward_time(module, name, tdict, iteration):
            _ts = time.time()
            y = module(x)
            _te = time.time()
            if iteration > 1: # warmup
                tdict[name].append(1000*(_te - _ts))  # in ms
            return y

        def _get_backward_time(module, name, inp, tdict, iteration):
            if isinstance(inp, th.Tensor):
                loss = y.sum()
            else:
                loss = list(y.values())[0].sum()
            _ts = time.time()
            loss.backward()
            _te = time.time()
            if iteration > 1: # warmup
                tdict[name].append(1000*(_te - _ts))  # in ms

        y = _get_forward_time(M0p, 'maxpool', Tforward, i)
        _get_backward_time(M0p, 'maxpool', y, Tbackward, i)

        y = _get_forward_time(M1, 'layer1', Tforward, i)
        _get_backward_time(M1, 'layer1', y, Tbackward, i)

        y = _get_forward_time(M2, 'layer2', Tforward, i)
        _get_backward_time(M2, 'layer2', y, Tbackward, i)

        y = _get_forward_time(M3, 'layer3', Tforward, i)
        _get_backward_time(M3, 'layer3', y, Tbackward, i)

        y = _get_forward_time(M4, 'layer4', Tforward, i)
        _get_backward_time(M4, 'layer4', y, Tbackward, i)

        y = _get_forward_time(M, 'fc', Tforward, i)
        _get_backward_time(M, 'fc', y, Tbackward, i)

    console.print('ResNet18 Forward Time (in ms)')
    console.print([(k, np.mean(v), np.std(v)) for (k, v) in Tforward.items()])
    console.print('ResNet18 Backward Time (in ms)')
    console.print([(k, np.mean(v), np.std(v)) for (k, v) in Tbackward.items()])


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--model', '-m', type=str, default='resnet18')
    ag.add_argument('--device', '-D', type=str,
        default='cuda' if th.cuda.is_available() else 'cpu')
    ag.add_argument('--maxiter', '-N', type=int, default=100)
    ag.add_argument('--batchsize', type=int, default=128)
    ag = ag.parse_args()

    check_resnet18(ag)
