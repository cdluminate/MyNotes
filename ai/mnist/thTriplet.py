#!/usr/bin/python3.7
'''
Simplified Triplet Network Implemented in PyTorch
:ref: https://github.com/andreasveit/triplet-network-pytorch
'''
import argparse
import os
import sys
from pprint import pprint

import torch as th
import torch.nn.functional as F


class Net(th.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = th.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = th.nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = th.nn.Dropout2d()
        self.fc1 = th.nn.Linear(320, 50)
        self.fc2 = th.nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        return self.fc2(x)


class Tripletnet(th.nn.Module):
    def __init__(self, embeddingnet):
        super(Tripletnet, self).__init__()
        self.embeddingnet = embeddingnet

    def forward(self, x, y, z):
        embedded_x = self.embeddingnet(x)
        embedded_y = self.embeddingnet(y)
        embedded_z = self.embeddingnet(z)
        dist_a = F.pairwise_distance(embedded_x, embedded_y, 2)
        dist_b = F.pairwise_distance(embedded_x, embedded_z, 2)
        return dist_a, dist_b, embedded_x, embedded_y, embedded_z


def loadMNIST():
    '''
    Load datasets and return dataset loaders
    '''
    raise NotImplementedError


if __name__ == '__main__':
    # parse arguments and dump
    ag = argparse.ArgumentParser()
    ag.add_argument('--batch', type=int, default=64)
    ag.add_argument('--epoch', type=int, default=10)
    ag.add_argument('--lr', type=float, default=1e-3)
    ag.add_argument('--cuda', action='store_true', default=False)
    ag.add_argument('--margin', type=float, default=0.2)
    ag.add_argument('--log', type=str, default='runs/XXX')
    ag = ag.parse_args()
    pprint(ag)

    # setup model and solver
    model = Net()
    print(model)
    triplet = Tripletnet(model)
    print(triplet)
    crit = th.nn.MarginRankingLoss(margin=ag.margin)
    print(crit)
    optim = th.optim.Adam(triplet.parameters(), lr=ag.lr)
    print(optim)
    print(sum([p.data.nelement() for p in triplet.parameters()]),
          'parameters in total.')

    # start learning!
    for eph in range(ag.epoch):
        for it, minibatch in enumerate(train_loader):
            # global iteration
            git = eph * len(train_loader) + it
            # train
            train_(triplet, crit, optim, minibatch, ag)

    # end of training
    print('EOT')


def train_(triplet, crit, optim, minibatch, ag) -> None:
    '''
    Perform one Forward-Backward-Update step.
    '''
    # forward pass and criterion
    triplet.train()
    d1, d2, d3 = minibatch
    distA, distB, embX, embY, embZ = triplet(d1, d2, d3)
    target = th.FloatTensor(distA.size()).fill_(1)
    loss_triplet = crit(distA, distB, target)
    loss_emb = embX.norm(2) + embY.norm(2) + embZ.norm(2)
    loss = loss_triplet + 0.001 * loss_emb

    # calculate accuracy
    pred = (distA - distB - 0.0).cpu()
    accu = (pred > 0).sum() * 1. / distA.size()[0]

    # backward
    optim.zero_grad()
    loss.backward()
    optim.step()
