'''
https://github.com/kuangliu/pytorch-cifar/blob/master/models/resnet.py

ResNet in PyTorch.
For Pre-activation ResNet, see 'preact_resnet.py'.
Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Deep Residual Learning for Image Recognition. arXiv:1512.03385

'''
import os
import torch as th
import collections
from . import cifar10, base
import yaml
from tqdm import tqdm
from termcolor import cprint, colored
from .utils import IMstd, IMmean, renorm, denorm

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import ct_res18
from .attacks import projectedGradientDescent


class Model(ct_res18.Model):
    def loss(self, x, y, *, adv=True): # NOTE, true by default
        # params
        alpha = 0.5
        #
        device = self.net.conv1.weight.device if not self.dataparallel else self.net.module.conv1.weight.device
        images, labels = x.to(device), y.to(device).view(-1)
        if not adv:
            output = self.forward(images)
            loss = th.nn.functional.cross_entropy(output, labels)
            return output, loss
        else:
            # baseline: forward original samples
            self.eval()
            with th.no_grad():
                output, loss = self.loss(images, labels, adv=False)
                acc_orig = (output.max(1)[1].eq(labels).sum().item()/len(y))
                loss_orig = loss.detach()
            # start PGD attack
            # (8/255 ~ 0.031) https://arxiv.org/pdf/1706.06083.pdf
            if np.random.random() >= 0.1:
                xr, r = projectedGradientDescent(self, images, labels,
                        eps=0.03, alpha=2./255., maxiter=7, verbose=False,
                        device=device, targeted=True, unbound=False, rinit=False)
                # forward the PGD adversary
                self.train()
                output, loss = self.loss(xr, labels, adv=False)
                loss = -loss
                acc_adv = (output.max(1)[1].eq(labels).sum().item()/len(y))
                loss_adv = loss.detach()
                # mandatory report
                print('\tRevAT|', colored('Orig loss', 'blue'),
                        '%.5f'%loss_orig, 'Acc', '%.3f'%acc_orig,
                        '|', colored('[Adv loss]', 'red'),
                        '%.5f'%loss.item(), 'Acc', '%.3f'%acc_adv)
                return (output, loss)
            xr, r = projectedGradientDescent(self, images, labels,
                    eps=0.03, alpha=2./255., maxiter=7, verbose=False,
                    device=device, targeted=False, unbound=False, rinit=False)
            # forward the PGD adversary
            self.train()
            output, loss = self.loss(xr, labels, adv=False)
            acc_adv = (output.max(1)[1].eq(labels).sum().item()/len(y))
            loss_adv = loss.detach()
            # mandatory report
            print('\t   AT|', colored('Orig loss', 'blue'),
                    '%.5f'%loss_orig, 'Acc', '%.3f'%acc_orig,
                    '|', colored('[Adv loss]', 'red'),
                    '%.5f'%loss.item(), 'Acc', '%.3f'%acc_adv)
            return (output, loss)
