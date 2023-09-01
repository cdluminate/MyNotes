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
    exp:
        x>0 py/px=exp(-x) y=-exp(-x) -> y=-exp(-x.sign(x))+c
        x<0 py/px=-exp(x) y=-exp(x)  --> y=-exp(-|x|)+c
    '''
    if losstype == 'flat':
        loss = y.view(-1).abs().mean()
    elif losstype == 'exp':
        loss = 1 + ((y.view(-1).abs() * -1).exp() * -1).mean()
    else:
        raise NotImplementedError
    return loss


@pytest.mark.parametrize('losstype', ('flat', 'exp'))
def test_pat_loss(losstype: str):
    y = th.rand(1,22,33,44)
    loss = pat_loss(y, losstype)
    print(loss)
    assert not th.isnan(loss)


def pat_resnet(model, i, j):
    # this is a dispatcher
    pass

def pat_resnet_from_x_to_bn1(model, x, losstype:str) -> th.Tensor:
    model_x_bn1 = IntermediateLayerGetter(model, {'bn1': 'bn1'})
    y = model_x_bn1(x)['bn1']
    loss = pat_loss(y, losstype)
    return x

@pytest.mark.parametrize('losstype', ('flat', 'exp'))
def test_pat_resnet_from_x_to_bn1(losstype: str):
    model = V.models.resnet18()
    x = th.rand(1,3,224,224)
    ptb = pat_resnet_from_x_to_bn1(model, x, losstype)


if __name__ == '__main__':
    model = V.models.resnet18()
    x = th.rand(1,3,224,224)
    pat_resnet_from_x_to_bn1(model, x)
