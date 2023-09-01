'''
ParetoAT implementation for ResNet
'''
import torch as th
import numpy as np
import torchvision as V
from torchvision.models._utils import IntermediateLayerGetter
import pytest


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
    else:
        raise NotImplementedError
    return loss


@pytest.mark.parametrize('losstype', ('flat', 'rflat', 'exp'))
def test_pat_loss(losstype: str):
    y = th.rand(1,22,33,44)
    loss = pat_loss(y, losstype)
    print(loss)
    assert not th.isnan(loss)


def pat_resnet(model: th.nn.Module, i: str, j: str, x: th.Tensor) -> th.Tensor:
    # this is a dispatcher
    IJLIST = ('x', 'bn1', 'maxpool', 'layer1', 'layer2', 'layer3', 'layer4', 'fc')
    assert i in IJLIST
    assert j in IJLIST
    assert IJLIST.index(i) < IJLIST.index(j)
    if (i, j) == ('x', 'bn1'):
        ptb = pat_resnet_from_x_to_bn1(model, x, 'flat')
    else:
        raise NotImplementedError
    return ptb


def pat_resnet_from_x_to_bn1(model, x, losstype:str, *, eps:float=4./255., numstep:int=3, stepsize:float=2./255.) -> th.Tensor:
    '''
    return the pat perturbation to x
    '''
    model_x_bn1 = IntermediateLayerGetter(model, {'bn1': 'bn1'})
    xr = x.clone().detach()
    xr.requires_grad = True
    for i in range(numstep):
        y = model_x_bn1(xr)['bn1']
        #print(f'{y.shape=}')
        loss = pat_loss(y, losstype)
        #print(f'{loss.shape=}', loss.item())
        gxr = th.autograd.grad(loss, xr)[0]
        #print(f'{gxr.shape=}')
        xr = xr - stepsize * th.sign(gxr)
        #xr = xr - stepsize * gxr * 2.0
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


if __name__ == '__main__':
    model = V.models.resnet50()
    x = th.rand(1,3,224,224)
    ptb = pat_resnet(model, 'x', 'bn1', x)
    xr = x + ptb
    print('xr', xr)
