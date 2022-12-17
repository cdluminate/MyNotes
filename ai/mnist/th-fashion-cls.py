#!/usr/bin/python3
'''
Pytorch, Fashion-Mnist Classification

Results
-------
* 7440HQ+940MX,CUDA9.0: ~1.0 ms/iteration, Model_v1 88% accuracy
'''
import sys
import os
import argparse
import json
from collections import OrderedDict
import random
import time
from statistics import mean

import numpy as np
import torch as th
from torch.utils.data import Dataset, DataLoader

from swish import *

# git clone https://github.com/zalandoresearch/fashion-mnist
sys.path.append("./fashion-mnist")
from utils import mnist_reader


# One-line timer function
def tic(): return eval("lambda: time.time() - {}".format(time.time()))


def makeVar(tensor):
    return th.autograd.Variable(tensor, requires_grad=False)


class MNISTDataset(Dataset):
    def __init__(self, X, Y):
        assert(X.shape[0] == Y.shape[0])
        self.X, self.Y = X, Y

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, index):
        x, y = self.X[index], self.Y[index]
        x = th.from_numpy(x/255.).float()
        y = th.LongTensor([int(y)])
        return x, y


class Model_v1(th.nn.Module):
    def __init__(self):
        super(Model_v1, self).__init__()
        self.seq1 = th.nn.Sequential(OrderedDict([
            ('ip1', th.nn.Linear(784, 256)),
            ('relu1', th.nn.ReLU()),
            ('ip2', th.nn.Linear(256, 10)),
        ]))

    def forward(self, x):
        x = self.seq1(x)
        return x


class Model_v2(th.nn.Module):
    def __init__(self):
        super(Model_v2, self).__init__()
        self.ip1 = th.nn.Linear(784, 256)
        self.sw1 = SwishModule()
        self.ip2 = th.nn.Linear(256, 10)

    def forward(self, x):
        x = self.ip1(x)
        x = self.sw1(x)
        x = self.ip2(x)
        return x


def evaluate(epoch, model, crit, testloader) -> None:
    losses = []
    accuracies = []
    for iteration, (xb, yb) in enumerate(testloader):
        model.eval()
        xb, yb = makeVar(xb), makeVar(yb).view(-1)
        xb, yb = (xb.cuda(), yb.cuda()) if ag.cuda else (xb, yb)

        output = model(xb)
        loss = crit(output, yb)

        # statistics
        pred = output.data.max(1)[1]
        correct = pred.eq(yb.data).sum()
        accuracy = correct / output.size(0)
        losses.append(loss.data[0])
        accuracies.append(accuracy)

    loss = mean(losses)
    accuracy = mean(accuracies)
    print('\033[KTest @', end=' ')
    print('Epoch {:>5d}'.format(epoch), end='\t|\t')
    print('loss {:>10.3f}'.format(loss), end='\t|\t')
    print('accu {:>9.4f}'.format(accuracy), end='\t|\t')
    print()


def main_train():

    print('<> Dataset')
    X_train, y_train = mnist_reader.load_mnist(
        'fashion-mnist/data/fashion', kind='train')
    X_test, y_test = mnist_reader.load_mnist(
        'fashion-mnist/data/fashion', kind='t10k')
    print(X_train.shape, y_train.shape)
    trainset = MNISTDataset(X_train, y_train)
    testset = MNISTDataset(X_test, y_test)
    trainloader = DataLoader(trainset, batch_size=ag.batch)
    testloader = DataLoader(testset, batch_size=ag.batch)
    print('training set shape', trainset.X.shape, trainset.Y.shape)
    print('    test set shape', testset.X.shape, testset.Y.shape)

    print('<> model')
    Model = Model_v2  # symlink
    model = Model().float().cuda() if ag.cuda else Model().float()
    print(model)

    crit = th.nn.CrossEntropyLoss()
    optimizer = th.optim.Adam(model.parameters(), lr=ag.lr, weight_decay=1e-5)

    # Main loop
    for epoch in range(ag.maxepoch):

        # [ test ]
        evaluate(epoch, model, crit, testloader)

        # [ train ]
        for iteration, (xb, yb) in enumerate(trainloader):
            model.train()
            xb, yb = makeVar(xb), makeVar(yb).view(-1)
            xb, yb = (xb.cuda(), yb.cuda()) if ag.cuda else (xb, yb)

            # periodical model test
            # if i % args.tp == 0:
            #  evaluation(i)
            # decay learning rate
            # if i > 1000:
            #  lr = args.lr * (0.5 ** ((i-1000)/2000))
            #  for param_group in optimizer.param_groups:
            #    param_group['lr'] = lr
            # forward, backward, update

            modelout = model(xb)
            loss = crit(modelout, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # report
            pred = modelout.data.max(1)[1]
            correct = pred.eq(yb.data).sum()
            accuracy = correct / modelout.size(0)
            print('\0337\033[K', end='')
            print('Train @', end=' ')
            print(f'Eph/Iter {epoch:>2d}/{iteration:>5d}'.format(iteration), end='\t|\t')
            print('loss {:>10.3f}'.format(loss.data[0]), end='\t|\t')
            print('accu {:>9.4f}'.format(accuracy), end='\t|\t')
            print('\0338', end='')
            sys.stdout.flush()


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.set_defaults(func=ag.print_help)
    subag = ag.add_subparsers()

    # [ train options ]
    ag_train = subag.add_parser('train')
    ag_train.set_defaults(func=main_train)
    ag_train.add_argument('-g', '--cuda', default=False, action='store_true')
    ag_train.add_argument('-m', '--maxepoch', type=int, default=10)
    ag_train.add_argument('-l', '--lr', type=float, default=1e-3)
    ag_train.add_argument('-b', '--batch', type=int, default=256)

    ag = ag.parse_args()
    print("-> Dump arguments")
    print(vars(ag))

    # [ Environment setup ]
    os.putenv('OPENBLAS_NUM_THREADS', '4')
    os.putenv('OMP_NUM_THREADS', '4')
    os.putenv('MKL_NUM_THREADS', '4')

    # [ Torch setup ]
    th.manual_seed(666)
    if ag.cuda:
        th.cuda.manual_seed(666)
    TENSOR_T = 'torch.cuda.FloatTensor' if ag.cuda else 'torch.FloatTensor'
    th.set_default_tensor_type(TENSOR_T)
    th.backends.cudnn.benchmark = True  # enable cuDNN auto-tuner

    ag.func()
