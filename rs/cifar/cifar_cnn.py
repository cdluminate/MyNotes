#!/usr/bin/env python3
# WIP
import sys
import os
import time
from collections import OrderedDict
import random
import argparse
import json
import math
from PIL import Image

import numpy as np
import torch as th
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Subset
import torchvision as vision

sys.path.append('..')
import FlashLight as fl


def parseArgs(argv, *, verbose=True):
    ag = argparse.ArgumentParser()
    ag.add_argument('--data', default='cifar10', choices=['cifar10', 'cifar100'])
    ag.add_argument('--cuda', default=False, action='store_true')
    ag.add_argument('--pool', type=str, default=os.path.expanduser('~/data'))
    ag.add_argument('--epoch', type=int, default=10)
    ag.add_argument('--lr', type=float, default=1e-3)
    ag.add_argument('--batch', type=int, default=64)
    ag.add_argument('--testevery', type=int, default=200)
    ag = ag.parse_args(argv)
    if verbose:
        print('=> Dump configuration')
        print(json.dumps(vars(ag), indent=2))
    return ag


def getDataLoaders(ag):
    T = vision.transforms
    transform = T.Compose([
        T.ToTensor(),
        ])
    dset_tr = vision.datasets.CIFAR10(root=ag.pool, train=True, transform=transform)
    dset_te = vision.datasets.CIFAR10(root=ag.pool, train=False, transform=transform)
    loader_tr = DataLoader(dset_tr, batch_size=ag.batch, shuffle=True, pin_memory=True, num_workers=3)
    loader_te = DataLoader(dset_te, batch_size=ag.batch, shuffle=False, pin_memory=True, num_workers=3)
    return loader_tr, loader_te


class Model(th.nn.Module):
    ''' Reference: caffe/examples/cifar10 # 70%
    https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10.py
    '''
    def __init__(self, ag):
        super(Model, self).__init__()
        self.SEQ1 = th.nn.Sequential(OrderedDict([

          ('conv1', th.nn.Conv2d(3, 32, 5, stride=1, padding=2)),
          ('bn1',   th.nn.BatchNorm2d(32)),
          ('relu1', th.nn.ReLU()),
          ('pool1', th.nn.MaxPool2d(3, stride=2, padding=1)),

          ('conv2', th.nn.Conv2d(32, 64, 5, stride=1, padding=2)),
          ('bn2',   th.nn.BatchNorm2d(64)),
          ('relu2', th.nn.ReLU()),
          ('pool2', th.nn.MaxPool2d(3, stride=2, padding=1)),

        ]))
        self.SEQ2 = th.nn.Sequential(OrderedDict([

          ('fc4',   th.nn.Linear(4096, 384)),
          ('bn4',   th.nn.BatchNorm1d(384)),
          ('relu4', th.nn.ReLU()),

          ('fc5',   th.nn.Linear(384, 192)),
          ('bn5',   th.nn.BatchNorm1d(192)),
          ('relu5', th.nn.ReLU()),

          ('fc6',   th.nn.Linear(192, int(ag.data.replace('cifar','')))),

        ]))
        th.nn.init.xavier_uniform_(self.SEQ1.conv1.weight, gain=1.414)
        th.nn.init.constant_(self.SEQ1.conv1.bias, 0.1)
    def forward(self, x):
        x = self.SEQ1(x)
        x = x.view(-1, 4096)
        x = self.SEQ2(x)
        return x


def evaluate(giter, net, crit, loader, *, ag):
    net.eval()
    total, correct, loss = 0, 0, 0
    with th.no_grad():
        for image, label in loader:
            image = image.cuda() if ag.cuda else image
            label = label.cuda() if ag.cuda else label
            out = net(image)
            l = crit(out, label)
            pred = out.data.max(1)[1]
            cor = pred.eq(label).detach().cpu().sum()
            total += label.nelement()
            correct += cor.item()
            loss += l.item()
            print('.', end='')
            sys.stdout.flush()
    accu = correct / total
    print()
    print(f'TEST [{giter}] loss {loss} accu {accu} ({correct}/{total})')


def train(model, loader_tr, loader_te, *, ag):
    '''
    train the given model on the given dataset
    '''
    crit = th.nn.CrossEntropyLoss()
    print(crit)
    optim = th.optim.Adam(model.parameters(), lr=ag.lr, weight_decay=1e-7)
    print(optim)

    for eph in range(ag.epoch):

        evaluate(eph*len(loader_tr), model, crit, loader_te, ag=ag)

        for liter, (image, label) in enumerate(loader_tr):
            net.train()
            giter = eph*len(loader_tr) + liter

            image = image.cuda() if ag.cuda else image
            label = label.cuda() if ag.cuda else label

            out = model(image)
            loss = crit(out, label)
            optim.zero_grad()
            loss.backward()
            optim.step()

            pred = out.data.max(1)[1]
            correct = pred.eq(label).detach().cpu().sum()
            accu = correct.item() / label.nelement()
            print(f'Eph[{eph}][{liter}/{len(loader_tr)}]', end='\t')
            print(f'loss {loss.item()}', end='\t')
            print(f'accu {accu} ({correct.item()}/{label.nelement()})')

            if (giter+1) % ag.testevery == 0:
                evaluate(eph*len(loader_tr), model, crit, loader_te, ag=ag)

    evaluate(eph*len(loader_tr), model, crit, loader_te, ag=ag)


if __name__ == '__main__':
    ag = parseArgs(sys.argv[1:])
    #fl.torchDefaultTensor('cuda/float' if ag.cuda else 'cpu/float')

    print('-> create model')
    net = Model(ag).cuda() if ag.cuda else Model(ag)
    print(net)

    print('-> Loading datasets')
    loader_tr, loader_te = getDataLoaders(ag)
    print(loader_tr, len(loader_tr))
    print(loader_te, len(loader_te))

    train(net, loader_tr, loader_te, ag=ag)

#    # decay the learning rate
#    if i>ag.decay0:
#        # $\eta = \eta_0 * 0.5 ^{ (i - i_0) / i_period }$
#        curlr = ag.lr * (0.5 ** ((i-ag.decay0)/ag.decayT))
#        if i>7500: curlr *= 0.1
#        for param_group in optimizer.param_groups:
#            param_group['lr'] = curlr
#            #print(param_group['lr'])
#

# random croping 28x28
# random mirroring
