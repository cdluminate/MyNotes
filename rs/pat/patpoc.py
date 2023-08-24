'''
POC for ParetoAT
https://pytorch.org/tutorials/recipes/recipes/benchmark.html

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
import torch.utils.benchmark as benchmark
import argparse
import time
import rich
from collections import defaultdict
from rich.progress import track
console = rich.get_console()

def benchmark_resnet(args):
    M = getattr(V.models, ag.model)().to(args.device)
    print(M)
    M0p = IntermediateLayerGetter(M, {'maxpool': 'maxpool'})
    M1 = IntermediateLayerGetter(M, {'layer1':'layer1'})
    M2 = IntermediateLayerGetter(M, {'layer2':'layer2'})
    M3 = IntermediateLayerGetter(M, {'layer3':'layer3'})
    M4 = IntermediateLayerGetter(M, {'layer4':'layer4'})

    results = []

    x = th.rand(args.batchsize, 3, 224, 224).to(args.device)
    x.requires_grad = True

    # maxpool forward
    M0p_forward = benchmark.Timer(stmt='y=M0p.forward(x)',
                                  globals={'x': x, 'M0p': M0p},
                                  description=ag.model,
                                  ).timeit(args.maxiter)
    console.print('M0p_forward', M0p_forward)
    results.append(M0p_forward)

    # maxpool backward
    y0p = list(M0p.forward(x).values())[0]
    M0p_backward = benchmark.Timer(stmt='y0p.sum().backward(retain_graph=True)',
                                   globals={'y0p': y0p},
                                   description=ag.model,
                                   ).timeit(args.maxiter)
    console.print('M0p_backward', M0p_forward)
    results.append(M0p_backward)

    # layer1 forward
    M1_forward = benchmark.Timer(stmt='y=M1.forward(x)',
                                 globals={'x': x, 'M1': M1},
                                 description=ag.model,
                                 ).timeit(args.maxiter)
    console.print('M1_forward', M1_forward)
    results.append(M1_forward)

    # layer1 backward
    y1 = list(M1.forward(x).values())[0]
    M1_backward = benchmark.Timer(stmt='y1.sum().backward(retain_graph=True)',
                                   globals={'y1': y1},
                                   description=ag.model,
                                   ).timeit(args.maxiter)
    console.print('M1_backward', M1_forward)
    results.append(M1_backward)

    # layer2 forward
    M2_forward = benchmark.Timer(stmt='y=M2.forward(x)',
                                 globals={'x': x, 'M2': M2},
                                 description=ag.model,
                                 ).timeit(args.maxiter)
    console.print('M2_forward', M2_forward)
    results.append(M2_forward)

    # layer2 backward
    y2 = list(M2.forward(x).values())[0]
    M2_backward = benchmark.Timer(stmt='y2.sum().backward(retain_graph=True)',
                                   globals={'y2': y2},
                                   description=ag.model,
                                   ).timeit(args.maxiter)
    console.print('M2_backward', M2_forward)
    results.append(M2_backward)

    # layer3 forward
    M3_forward = benchmark.Timer(stmt='y=M3.forward(x)',
                                 globals={'x': x, 'M3': M3},
                                 description=ag.model,
                                 ).timeit(args.maxiter)
    console.print('M3_forward', M3_forward)
    results.append(M3_forward)

    # layer3 backward
    y3 = list(M3.forward(x).values())[0]
    M3_backward = benchmark.Timer(stmt='y3.sum().backward(retain_graph=True)',
                                   globals={'y3': y3},
                                   description=ag.model,
                                   ).timeit(args.maxiter)
    console.print('M3_backward', M3_forward)
    results.append(M3_backward)

    # layer4 forward
    M4_forward = benchmark.Timer(stmt='y=M4.forward(x)',
                                 globals={'x': x, 'M4': M4},
                                 description=ag.model,
                                 ).timeit(args.maxiter)
    console.print('M4_forward', M4_forward)
    results.append(M4_forward)

    # layer4 backward
    y4 = list(M4.forward(x).values())[0]
    M4_backward = benchmark.Timer(stmt='y4.sum().backward(retain_graph=True)',
                                   globals={'y4': y4},
                                   description=ag.model,
                                   ).timeit(args.maxiter)
    console.print('M4_backward', M4_forward)
    results.append(M4_backward)

    # M forward
    M_forward = benchmark.Timer(stmt='y=M.forward(x)',
                                 globals={'x': x, 'M': M},
                                 description=ag.model,
                                 ).timeit(args.maxiter)
    console.print('M_forward', M_forward)
    results.append(M_forward)

    # M backward
    y = M.forward(x)
    M_backward = benchmark.Timer(stmt='y.sum().backward(retain_graph=True)',
                                   globals={'y': y},
                                   description=ag.model,
                                   ).timeit(args.maxiter)
    console.print('M_backward', M_forward)
    results.append(M_backward)

    # compare
    compare = benchmark.Compare(results)
    compare.print()


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--model', '-m', type=str, default='resnet18')
    ag.add_argument('--device', '-D', type=str,
        default='cuda' if th.cuda.is_available() else 'cpu')
    ag.add_argument('--maxiter', '-N', type=int, default=100)
    ag.add_argument('--batchsize', type=int, default=128)
    ag = ag.parse_args()

    if 'resnet' in ag.model:
        benchmark_resnet(ag)
    else:
        raise NotImplementedError
