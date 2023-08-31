'''
ParetoAT implementation for ResNet
'''
import torch as th
import numpy as np
import torchvision as V
from torchvision.models._utils import IntermediateLayerGetter


def pat_resnet(model, i, j):
    # this is a dispatcher
    pass

def pat_resnet_from_x_to_bn1(model, x, loss:str='negsum'):
    model_x_bn1 = IntermediateLayerGetter(model, {'bn1': 'bn1'})
    y = model_x_bn1(x)['bn1']
    print(y.shape)

if __name__ == '__main__':
    model = V.models.resnet18()
    x = th.rand(1,3,224,224)
    pat_resnet_from_x_to_bn1(model, x)
