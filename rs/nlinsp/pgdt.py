import functools as ft
import math
import numpy as np
import os
import sys
import re
import random
import statistics
import torch as th
import torch.nn.functional as F
import torchvision as V
import json
import rich
console = rich.get_console()


IMmean = th.tensor([0.485, 0.456, 0.406])
IMstd = th.tensor([0.229, 0.224, 0.225])


renorm = lambda im: im.sub(IMmean[:,None,None].to(im.device)).div(IMstd[:,None,None].to(im.device))
denorm = lambda im: im.mul(IMstd[:,None,None].to(im.device)).add(IMmean[:,None,None].to(im.device))


def BIM_l8_T(model, images, labels, *, eps=8./255., alpha=2./255., maxiter=6, verbose=False):
    '''
    model should have the classification head.
    the images are always in [0, 1].
    the images are using imagenet normalizations.
    '''
    model.eval()
    device = images.device
    images_orig = images.clone().detach()
    labels_orig = labels.clone().detach()
    images = images.clone().detach()
    traj = [renorm(images_orig.clone()).detach()]
    batch_size = images.shape[0]
    for _ in range(maxiter):
        images.requires_grad = True
        outputs = model.forward(images)
        loss = F.cross_entropy(outputs, labels)
        if verbose:
            console.print('>', 'loss', loss.item())
        grad = th.autograd.grad(loss, images,
                                retain_graph=False,
                                create_graph=False)[0]
        images = images.detach() + alpha * grad.sign()
        diff = th.clamp(images - images_orig, min=-eps, max=+eps).detach()
        images = th.clamp(images_orig + diff, min=0., max=1.).detach()
        traj.append(renorm(images.clone()).detach())
    traj = th.stack(traj)
    return traj


if __name__ == '__main__':
    #model = V.models.resnet18(weights=V.models.ResNet18_Weights.DEFAULT)
    model = V.models.resnet18(weights=None)
    images = th.rand(1, 3, 224, 224)
    labels = th.tensor([0])
    traj = BIM_l8_T(model, images, labels, verbose=True)
    print(traj.shape)
    traj = traj.view(traj.shape[0], -1)
    cos = F.normalize(traj)
    cos = 1.0 - th.cdist(cos, cos)
    print(cos)
