'''
POC for ParetoAT

Pytorch's official benchmarking tool is not designed for
benchmarking forward + backward time. They do not provide
a post-stmt procedure for us to clear the gradients.
As a result, the loop will break at the second iteration
becasue we repetitively conduct backward on the same graph.
If we toggle retain_graph=True, then the CUDA memory will
boom very quickly. It is much worse than the naive tic;toc
solution for this case.
https://pytorch.org/docs/stable/benchmark_utils.html

Quadro RTX 8000
resnet18 Forward Time (in ms)
[
    ('maxpool', 0.4289296208595743, 0.18836048810791495),
    ('layer1', 1.1388233729771204, 0.2946200831345),
    ('layer2', 1.8534587354076153, 0.4209195214446256),
    ('layer3', 2.4907102390211455, 0.36688549494364375),
    ('layer4', 3.2006331852504184, 0.5328783730295088),
    ('fc', 3.3979951118936342, 0.6263093935695332)
]
resnet18 Backward Time (in ms)
[
    ('maxpool', 0.9693880470431581, 0.05998365498622745),
    ('layer1', 2.610554500501983, 0.1751502804680237),
    ('layer2', 4.682553057767907, 0.6908200035028613),
    ('layer3', 6.543899069027025, 0.6494526993364088),
    ('layer4', 8.41982024056571, 0.9969388130910507),
    ('fc', 9.016268107355858, 0.9424347560009347)
]
resnet50 Forward Time (in ms)
[
    ('maxpool', 0.4012146774603396, 0.012888487628937881),
    ('layer1', 1.8081713695915378, 0.35808031011092645),
    ('layer2', 3.3599211245167013, 0.5033862663830285),
    ('layer3', 5.782290380828234, 0.7655593008217881),
    ('layer4', 6.938289622871244, 0.7443712683003231),
    ('fc', 7.178099787965113, 0.7908687621752492)
]
resnet50 Backward Time (in ms)
[
    ('maxpool', 0.9794040602080676, 0.15300795347766394),
    ('layer1', 4.837897359108438, 0.7438671314668647),
    ('layer2', 9.632042476109095, 0.9017258090230915),
    ('layer3', 15.969196144415408, 1.4968684903718796),
    ('layer4', 11.342936632584552, 5.927833271585824),
    ('fc', 12.277712627333038, 6.070480839370469)
]
resnet152 Forward Time (in ms)
[
    ('maxpool', 0.4045476718824737, 0.016725994703391613),
    ('layer1', 1.8668150415225906, 0.4290146634324549),
    ('layer2', 5.120036553363411, 0.9116659495300263),
    ('layer3', 18.873200124623825, 1.294210531446655),
    ('layer4', 20.020078639594875, 1.3914365803505786),
    ('fc', 20.24290269734908, 1.3467628275885557)
]
resnet152 Backward Time (in ms)
[
    ('maxpool', 0.9799465841176559, 0.1096111827556811),
    ('layer1', 4.653497618071887, 0.25362137995997985),
    ('layer2', 13.963536340363172, 1.0371340444976456),
    ('layer3', 472.6531724540555, 2.0603697936399716),
    ('layer4', 538.6889297135023, 1.505575611767354),
    ('fc', 540.628550003986, 1.3324467197425678)
]
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

def check_resnet(args):
    M = getattr(V.models, ag.model)().to(args.device)
    print(M)
    M0p = IntermediateLayerGetter(M, {'maxpool': 'maxpool'})
    M1 = IntermediateLayerGetter(M, {'layer1':'layer1'})
    M2 = IntermediateLayerGetter(M, {'layer2':'layer2'})
    M3 = IntermediateLayerGetter(M, {'layer3':'layer3'})
    M4 = IntermediateLayerGetter(M, {'layer4':'layer4'})
    Tforward = defaultdict(list)
    Tbackward = defaultdict(list)

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

    for i in track(range(args.maxiter), description='maxpool'):
        x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True
        y = _get_forward_time(M0p, 'maxpool', Tforward, i)
        _get_backward_time(M0p, 'maxpool', y, Tbackward, i)

    for i in track(range(args.maxiter), description='layer1'):
        x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True
        y = _get_forward_time(M1, 'layer1', Tforward, i)
        _get_backward_time(M1, 'layer1', y, Tbackward, i)

    for i in track(range(args.maxiter), description='layer2'):
        x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True
        y = _get_forward_time(M2, 'layer2', Tforward, i)
        _get_backward_time(M2, 'layer2', y, Tbackward, i)

    for i in track(range(args.maxiter), description='layer3'):
        x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True
        y = _get_forward_time(M3, 'layer3', Tforward, i)
        _get_backward_time(M3, 'layer3', y, Tbackward, i)

    for i in track(range(args.maxiter), description='layer4'):
        x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True
        y = _get_forward_time(M4, 'layer4', Tforward, i)
        _get_backward_time(M4, 'layer4', y, Tbackward, i)

    for i in track(range(args.maxiter), description='fc'):
        x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True
        y = _get_forward_time(M, 'fc', Tforward, i)
        _get_backward_time(M, 'fc', y, Tbackward, i)

    console.print(f'{args.model} Forward Time (in ms)')
    console.print([(k, np.mean(v), np.std(v)) for (k, v) in Tforward.items()])
    console.print(f'{args.model} Backward Time (in ms)')
    console.print([(k, np.mean(v), np.std(v)) for (k, v) in Tbackward.items()])


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--model', '-m', type=str, default='resnet18')
    ag.add_argument('--device', '-D', type=str,
        default='cuda' if th.cuda.is_available() else 'cpu')
    ag.add_argument('--maxiter', '-N', type=int, default=100)
    ag.add_argument('--batchsize', type=int, default=128)
    ag = ag.parse_args()

    if 'resnet' in ag.model:
        check_resnet(ag)
    else:
        raise NotImplementedError
