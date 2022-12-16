import os
import torch as th

def spre(mod: th.nn.Module, antic: bool=False):
    '''
    Defensive Spectrum Regularization

    arguments:
        mod: a torch module instance
        antic: toggle anti-collapse
    '''

    if isinstance(mod, th.nn.Linear):

        # [slow version]
        # A, Ap = mod.weight, th.pinverse(mod.weight)
        #svdA, svdAp = th.svd(A), th.svd(Ap)
        #σ, σp = svdA.S.max(), svdAp.S.max()
        # [fast version]
        svdA = th.svd(mod.weight)
        σ, σp = svdA.S.max(), 1/svdA.S.min()

        sr = th.log(σ * σ * σp + 1.0).relu()
        if antic:
            sr += th.log(1e-2/svdA.S.min()).relu()
        #print('S.max', svdA.S.max().item(), 'S.min', svdA.S.min().item())
    else:
        raise TypeError(mod)
    return sr


def zeta(output: th.Tensor):
    '''
    Lifting the lowerbound of Zeta
    '''
    assert(len(output.shape) == 2)
    top2v = th.topk(output, 2, dim=1, largest=True)[0]
    top2vm = top2v.mean(dim=1).view(-1, 1)
    norm = (top2v - top2vm).norm(p=2, dim=1).mean()
    lz = -th.log(norm)  # increase norm
    return lz
