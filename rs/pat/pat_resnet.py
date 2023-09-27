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
from typing import *
import os
import sys
import torch as th
import numpy as np
import torchvision as V
import torch.nn.functional as F
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
# local
import ilsvrc

__NAMES__ = ('x', 'relu', 'layer1', 'layer2', 'layer3', 'layer4', 'fc')


def get_names(idx:int = None):
    if idx is not None:
        return __NAMES__[idx]
    else:
        return __NAMES__


def pat_forward(r50: th.nn.Module,
                src: Union[str, int],
                tgt: Union[str, int],
                x: th.Tensor,
                *,
                return_dict: bool=False):
    names = ('x', 'relu', 'layer1', 'layer2', 'layer3', 'layer4', 'fc')
    src = names[src] if isinstance(src, int) else src
    tgt = names[tgt] if isinstance(tgt, int) else tgt
    assert src in names, f'unknown source: {src}'
    assert tgt in names, f'unknown target: {tgt}'
    assert names.index(src) < names.index(tgt), f'illegal source-target combination {src}:{tgt}'
    ydict = {}
    # part 1
    if names.index(src) < names.index('relu'):
        # x bound is (0, 1)
        x = ilsvrc.NORMALIZE(x)
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


@pytest.mark.parametrize('losstype', ('flat', 'rflat', 'exp', 'mix'))
def test_pat_loss(losstype: str):
    y = th.rand(1,22,33,44)
    loss = pat_loss(y, losstype)
    print(loss)
    assert not th.isnan(loss)


class ParetoAT(object):
    def __init__(self, model):
        self.normalize = ilsvrc.NORMALIZE
        self.model = model
    def __call__(self, i, j, x, y) -> th.Tensor:
        return self.forward(i, j, x, y)
    def forward(self, i: int, j: int, x: th.Tensor, y: th.Tensor) -> th.Tensor:
        '''
        adversarial version of x
        '''
        assert all([i > 0, j > 0, i < j, i < len(__NAMES__), j < len(__NAMES__)])
        src, tgt = get_names(i), get_names(j)


# XXX: rewrite
def pat_resnet(model: th.nn.Module, runningstat: object,
               i: str, j: str,
               x: th.Tensor, y: th.Tensor) -> th.Tensor:
    # this is a dispatcher
    assert all([i > 0, j > 0, i < j, i < len(__NAMES__), j < len(__NAMES__)])
    src, tgt = get_names(i), get_names(j)
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


def pat_resnet_from_x_to_any(model: th.nn.Module,
                             i: int, j: int,
                             x: th.Tensor, y: th.Tensor,
                             *,
                             losstype: str = 'mix',
                             eps: float = 6./255.,
                             numstep: int = 3,
                             stepsize: float=2./255.) -> th.Tensor:
    '''
    return perturbation
    '''
    xr = x.clone().detach()
    xr.requires_grad = True
    assert i == 0
    for niter in range(numstep):
        output = pat_forward(model, i, j, xr)
        if get_names(j) == 'fc':
            loss = -F.cross_entropy(output, y)
            #print(f'DEBUG: {i},{j} using CE', loss.item())
        else:
            loss = pat_loss(output, losstype)
            #print(f'DEBUG: {i},{j} using PAT_LOSS')
        gxr = th.autograd.grad(loss, xr)[0]
        xr = xr - stepsize * th.sign(gxr) # PGD
        xr = xr.clamp(min=x - eps, max=x + eps)
        xr = xr.clamp(min=0., max=1.)
        xr = xr.clone().detach()
        xr.requires_grad = True
    return (xr - x).clone().detach()


@pytest.mark.parametrize('j,losstype', it.product(range(1, len(__NAMES__)),
                                                  ('flat', 'rflat', 'exp', 'mix')))
def test_pat_resnet_from_x_to_any(j, losstype):
    model = V.models.resnet50()
    x = th.rand(1, 3, 224, 224)
    y = th.randint(1000, (1,))
    ptb = pat_resnet_from_x_to_any(model, 0, j, x, y, losstype=losstype)
    print(f'{6./255.=}', f'{ptb.mean()=}', f'{ptb.min()=}', f'{ptb.max()=}', f'{ptb.std()=}')
    assert ptb.min() >= -6./255.
    assert ptb.max() <= 6./255.
    xr = x + ptb
    print(f'{6./255.=}', f'{xr.mean()=}', f'{xr.min()=}', f'{xr.max()=}', f'{xr.std()=}')
    assert xr.min() >= 0.0
    assert xr.max() <= 1.0


class ParetoAT_R1(object):
    '''
    Automatic wrapper
    '''
    def __init__(self, p_path: str, losstype:str='mix'):
        console.log(f'>_< ParetoAT_R1: initialize using {p_path}')
        self.p = np.loadtxt(p_path)
        self.losstype = losstype
    def __call__(self, model, x, y):
        j = pat_sample_r1(self.p)
        #print(f'>_< ParetoAT_R1: (i,j)=({0},{j})')
        ptb = pat_resnet_from_x_to_any(model, 0, j, x, y, losstype=self.losstype)
        return ptb


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


def pat_solve_row1(args) -> np.ndarray:
    tau = np.zeros(6)
    p = np.ones(6) / 6.
    rho = args.solve_rho
    eta = args.solve_eta
    tmp = np.loadtxt(args.benchmark_save)
    for i in range(1, len(__NAMES__)):
        tau[i-1] = tmp[0, i]
    omega = tmp[0, 6]
    console.print('tau:', tau)
    console.print('eta:', eta)
    console.print('rho:', rho)
    console.print('omega:', omega)
    console.print('rho.omega:', rho*omega)
    from scipy.optimize import lsq_linear
    A = np.ones([2, 6])
    A[1, :] = tau
    b = np.array([1, rho*omega]).T
    console.print('A:', A)
    console.print('b:', b)
    sol = lsq_linear(A, b, bounds=(0., 1.))
    console.print('x:', sol.x)
    console.print('x.tau:', (sol.x*tau).sum())
    console.print('x.sum:', sol.x.sum())
    return sol.x


def pat_sample(p: np.ndarray) -> (int, int):
    '''
    sample (i, j) from prob mass matrix
    '''
    assert len(p.shape) == 2
    pool = []
    prob = []
    for (i, j) in it.product(range(p.shape[0]), range(p.shape[1])):
        # upper triangular
        if i >= j:
            continue
        pool.append((i, j))
        prob.append(p[i, j])
    sel = np.random.choice(len(prob), p=prob)
    return pool[sel]


@pytest.mark.skipif(not os.path.exists('pat_r50_p_0.2.txt'),
                    reason='P matrix not found')
def test_pat_sample():
    p = np.loadtxt('pat_r50_p_0.2.txt')
    for i in range(10000):
        i, j = pat_sample(p)
        print(i, j)
        assert all([i < j, i >= 0, i < 7, j > 0, j <= 7])


def pat_sample_r1(p: np.ndarray) -> int:
    assert len(p.shape) == 1
    sel = np.random.choice(len(p), p=p)
    return sel + 1


@pytest.mark.skipif(not os.path.exists('pat_r50_pr1_0.2.txt'),
                    reason='P vector not found')
def test_pat_sample_r1():
    p = np.loadtxt('pat_r50_pr1_0.2.txt')
    for i in range(10000):
        i, j = 0, pat_sample_r1(p)
        print(i, j)
        assert all([i < j, i >= 0, i < 7, j > 0, j <= 7])


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
    ag.add_argument('--solve_save', type=str, default='pat_r50_p_0.2.txt')
    # solve_r1 (only the first row)
    ag.add_argument('--solve_r1', '-R', action='store_true')
    ag.add_argument('--solve_r1_save', type=str, default='pat_r50_pr1_0.2.txt')
    # parse
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
    elif ag.solve_r1:
        vector = pat_solve_row1(ag)
        console.print(vector)
        np.savetxt(ag.solve_r1_save, vector, fmt='%.8f')
        console.log(f'vector written into {ag.solve_r1_save}')
    else:
        console.print('No action specified')
