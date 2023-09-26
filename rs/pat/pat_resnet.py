'''
ParetoAT POC and implementation for ResNet

Pytorch's official benchmarking tool is not designed for
benchmarking forward + backward time. They do not provide
a post-stmt procedure for us to clear the gradients.
As a result, the loop will break at the second iteration
becasue we repetitively conduct backward on the same graph.
If we toggle retain_graph=True, then the CUDA memory will
boom very quickly. It is much worse than the naive tic;toc
solution for this case.
https://pytorch.org/docs/stable/benchmark_utils.html
'''
import torch as th
import numpy as np
import torchvision as V
from torchvision.models._utils import IntermediateLayerGetter
import pytest
import random
import functools as ft
import itertools as it
import argparse
import time
import rich
console = rich.get_console()
from rich.progress import track

__NAMES__ = ('x', 'relu', 'layer1', 'layer2', 'layer3', 'layer4', 'fc')

def pat_forward(r50: th.nn.Module,
                src: str,
                tgt: str,
                x: th.Tensor,
                *,
                return_dict: bool=False):
    names = ('x', 'relu', 'layer1', 'layer2', 'layer3', 'layer4', 'fc')
    assert src in names, 'unknown source'
    assert tgt in names, 'unknown target'
    assert names.index(src) < names.index(tgt), 'illegal source-target combination'
    ydict = {}
    # part 1
    if names.index(src) < names.index('relu'):
        x = r50.conv1(x)
        x = r50.bn1(x)
        x = r50.relu(x)
        ydict.update({'relu': x})
    if names.index(tgt) == names.index('relu'):
        return ydict if return_dict else x
    # part 2
    if names.index(src) < names.index('layer1'):
        x = r50.maxpool(x)
        x = r50.layer1(x)
        ydict.update({'layer1': x})
    if names.index(tgt) == names.index('layer1'):
        return ydict if return_dict else x
    # part 3
    if names.index(src) < names.index('layer2'):
        x = r50.layer2(x)
        ydict.update({'layer2': x})
    if names.index(tgt) == names.index('layer2'):
        return ydict if return_dict else x
    # part 4
    if names.index(src) < names.index('layer3'):
        x = r50.layer3(x)
        ydict.update({'layer3': x})
    if names.index(tgt) == names.index('layer3'):
        return ydict if return_dict else x
    # part 5
    if names.index(src) < names.index('layer4'):
        x = r50.layer4(x)
        ydict.update({'layer4': x})
    if names.index(tgt) == names.index('layer4'):
        return ydict if return_dict else x
    # part 6
    if names.index(src) < names.index('fc'):
        x = r50.avgpool(x)
        x = th.flatten(x, 1)
        x = r50.fc(x)
        ydict.update({'fc': x})
    if names.index(tgt) == names.index('fc'):
        return ydict if return_dict else x
    # exception
    raise Exception('Why is the function not yet returned?')


@pytest.mark.parametrize('src,tgt', it.product(__NAMES__, reversed(__NAMES__)))
def test_pat_forward(src, tgt):
    if __NAMES__.index(src) >= __NAMES__.index(tgt):
        return
    model = V.models.resnet50(num_classes=1000)
    model.eval()
    x = th.rand(1, 3, 224, 224)
    if src != 'x':
        x = pat_forward(model, 'x', src, x)
    y = pat_forward(model, src, tgt, x)



def pat_loss(y: th.Tensor, losstype: str) -> th.Tensor:
    '''
    pat_loss can be used on any intermediate feature, except for
    the last layer which is dealt with cross entropy loss.
    y: any-shape feature map
    losstype: (flat, exp)
    flat:
        x>0 py/px=+1 y=x.sign(x) -> y=|x|+c
        x<0 py/px=-1 y=x.sign(x)
    rflat:
        reverse flat.
    exp:
        x>0 py/px=exp(-x) y=-exp(-x) -> y=-exp(-x.sign(x))+c
        x<0 py/px=-exp(x) y=-exp(x)  --> y=-exp(-|x|)+c
    '''
    if losstype == 'flat':
        loss = y.view(-1).abs().sum()
    elif losstype == 'rflat':
        loss = -y.view(-1).abs().sum()
    elif losstype == 'exp':
        loss = 1 + ((y.view(-1).abs() * -1).exp() * -1).sum()
    elif losstype == 'mix':
        losstype = random.choice(['flat', 'rflat', 'exp'])
        return pat_loss(y, losstype)
    else:
        raise NotImplementedError
    return loss


@pytest.mark.parametrize('losstype', ('flat', 'rflat', 'exp'))
def test_pat_loss(losstype: str):
    y = th.rand(1,22,33,44)
    loss = pat_loss(y, losstype)
    print(loss)
    assert not th.isnan(loss)


def pat_resnet(model: th.nn.Module, i: str, j: str, x: th.Tensor, normalize=None) -> th.Tensor:
    # this is a dispatcher
    assert all([i > 0, j > 0, i < j, i < len(__NAMES__), j < len(__NAMES__)])
    raise NotImplementedError
    IJLIST = ('x', 'bn1', 'maxpool', 'layer1', 'layer2', 'layer3', 'layer4', 'fc')
    assert i in IJLIST
    assert j in IJLIST
    assert IJLIST.index(i) < IJLIST.index(j)
    if (i, j) == ('x', 'bn1'):
        ptb = pat_resnet_from_x_to_bn1(model, x, 'mix', normalize=normalize)
    else:
        raise NotImplementedError
    return ptb


def pat_resnet_from_x_to_bn1(model, x, losstype:str, *,
                             normalize:callable=None,
                             eps:float=6./255.,
                             numstep:int=3,
                             stepsize:float=2./255.) -> th.Tensor:
    '''
    return the pat perturbation to x
    '''
    model_x_bn1 = IntermediateLayerGetter(model, {'bn1': 'bn1'})
    xr = x.clone().detach()
    xr.requires_grad = True
    for i in range(numstep):
        if normalize is not None:
            xr = normalize(xr)
        loss = pat_loss(model_x_bn1(xr)['bn1'], losstype)
        gxr = th.autograd.grad(loss, xr)[0]
        xr = xr - stepsize * th.sign(gxr)  # XXX: PGD
        #xr = xr - stepsize * gxr * 2.0  # XXX: GD
        xr = xr.clamp(min=x - eps, max=x + eps)
        xr = xr.clamp(min=0.0, max=1.0)
        xr = xr.clone().detach()
        xr.requires_grad = True
    return (xr - x).clone().detach()


@pytest.mark.parametrize('losstype', ('flat', 'rflat', 'exp'))
def test_pat_resnet18_from_x_to_bn1(losstype: str):
    model = V.models.resnet18()
    x = th.rand(1,3,224,224)
    ptb = pat_resnet_from_x_to_bn1(model, x, losstype, eps=4./255.)
    print(f'{4./255.=}')
    print(f'{ptb.mean()=}')
    print(f'{ptb.min()=}')
    print(f'{ptb.max()=}')
    print(f'{ptb.std()=}')
    assert ptb.min() >= -4./255.
    assert ptb.max() <= 4./255.
    xr = x + ptb
    print(f'{4./255.=}')
    print(f'{xr.mean()=}')
    print(f'{xr.min()=}')
    print(f'{xr.max()=}')
    print(f'{xr.std()=}')
    assert xr.min() >= 0.0
    assert xr.max() <= 1.0


@pytest.mark.parametrize('losstype', ('flat', 'rflat', 'exp'))
def test_pat_resnet50_from_x_to_bn1(losstype: str):
    model = V.models.resnet50()
    x = th.rand(1,3,224,224)
    ptb = pat_resnet_from_x_to_bn1(model, x, losstype, eps=4./255.)
    print(f'{4./255.=}')
    print(f'{ptb.mean()=}')
    print(f'{ptb.min()=}')
    print(f'{ptb.max()=}')
    print(f'{ptb.std()=}')
    assert ptb.min() >= -4./255.
    assert ptb.max() <= 4./255.
    xr = x + ptb
    print(f'{4./255.=}')
    print(f'{xr.mean()=}')
    print(f'{xr.min()=}')
    print(f'{xr.max()=}')
    print(f'{xr.std()=}')
    assert xr.min() >= 0.0
    assert xr.max() <= 1.0


def get_forward_backward_time(model, src, tgt, args) -> float:
    tm = []
    optim = th.optim.SGD(model.parameters(), lr=0.0)
    for i in range(args.benchmark_niter + 3):
        # first three rounds are warmup
        x = th.rand(args.benchmark_batchsize, 3, 224, 224).to(args.device)
        x.requires_grad = True
        orig_x = x
        if src != 'x':
            x = pat_forward(model, 'x', src, x)
        # forward
        th.cuda.synchronize()
        tm_forward_start = time.time()
        x = pat_forward(model, src, tgt, x)
        th.cuda.synchronize()
        tm_forward_end = time.time()
        # loss
        loss = x.sum()
        optim.step()
        # backward
        th.cuda.synchronize()
        tm_backward_start = time.time()
        loss.backward()
        th.cuda.synchronize()
        tm_backward_end = time.time()
        assert orig_x.grad is not None
        # log
        tmi = (tm_backward_end - tm_backward_start) + (tm_forward_end - tm_forward_start)
        tm.append(tmi)
    return np.mean(tm[3:])


def pat_benchmark(args) -> np.ndarray:
    console.log('Initializing...')
    mat = np.zeros([len(__NAMES__), len(__NAMES__)]) # from/to
    model = getattr(V.models, args.arch)().to(args.device)
    model.eval()
    console.log('Benchmarking...')
    for ((i, src), (j, tgt)) in it.product(enumerate(__NAMES__), enumerate(__NAMES__)):
        if i >= j:
            continue
        tmij = get_forward_backward_time(model, src, tgt, args)
        console.log('F-B:', i, src.ljust(7), j, tgt.ljust(7), tmij)
        mat[i, j] = tmij
    return mat


def pat_solve(args) -> np.ndarray:
    console.log('load tau and init p ...')
    tau = np.zeros(21)
    p = np.ones(21) / 21.
    rho = args.solve_rho
    eta = args.solve_eta
    # fill in the vector
    tmp = np.loadtxt(args.benchmark_save)
    k = 0
    for (i, j) in it.product(range(len(__NAMES__)), range(len(__NAMES__))):
        if i >= j:
            continue
        tau[k] = tmp[i,j]
        k += 1
    omega = tmp[0,6]
    console.print('tau:', tau)
    console.print('p:', p)
    console.print('eta:', eta)
    console.print('rho:', rho)
    console.print('omega:', omega)
    console.print('rho.omega:', rho*omega)
    # solve
    console.log('solve x for Ax=b ...')

    from scipy.optimize import lsq_linear
    A = np.ones([2, 21])
    A[1,:] = tau
    b = np.array([1, rho * omega]).T
    console.print('A', A)
    console.print('b', b)
    sol = lsq_linear(A, b, bounds=(0., 1.))
    console.print('x', sol.x)
    console.print('x.tau', (sol.x*tau).sum())
    console.print('x.sum', sol.x.sum())
    #
    res = np.zeros([7, 7])
    k = 0
    for (i, j) in it.product(range(7), range(7)):
        if i >= j:
            continue
        res[i,j] = sol.x[k]
        k += 1
    return res


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    # global
    ag.add_argument('--arch', type=str, default='resnet50')
    ag.add_argument('--device', type=str, default='cuda' if th.cuda.is_available() else 'cpu')
    # benchmark
    ag.add_argument('--benchmark', '-B', action='store_true')
    ag.add_argument('--benchmark_batchsize', type=int, default=128)
    ag.add_argument('--benchmark_niter', type=int, default=100)
    ag.add_argument('--benchmark_save', type=str, default='pat_r50_tau.txt')
    # solve
    ag.add_argument('--solve', '-S', action='store_true')
    ag.add_argument('--solve_rho', type=float, default=0.2)
    ag.add_argument('--solve_eta', type=float, default=3.0)
    ag.add_argument('--solve_niter', type=int, default=1000)
    ag.add_argument('--solve_save', type=str, default='pat_r50_p_0.2.txt')
    ag = ag.parse_args()

    if ag.benchmark:
        matrix = pat_benchmark(ag)
        console.print(matrix)
        np.savetxt(ag.benchmark_save, matrix, fmt='%.6f')
        console.log(f'matrix written into {ag.benchmark_save}')
    elif ag.solve:
        matrix = pat_solve(ag)
        console.print(matrix)
        np.savetxt(ag.solve_save, matrix, fmt='%.8f')
        console.log(f'matrix written into {ag.solve_save}')
    else:
        console.print('No action specified')

    #model = V.models.resnet50()
    #x = th.rand(1,3,224,224)
    #ptb = pat_resnet(model, 'x', 'bn1', x)
    #xr = x + ptb
    #print('xr', xr)
