'''
P2V using PyTorch
Copyright (C) 2018 Mo Zhou
'''
import os
import sys
import argparse
from PIL import Image
from pprint import pprint
import numpy as np
import pylab
import json
import tqdm
import pickle
import random

import torch as th
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
import torchvision as vision
from scipy.stats import pearsonr


def imRead(fpath, transform=None):
    img = Image.open(fpath).convert('RGB')
    if transform == 'resize':
        trans = T.Compose([
            T.Resize((81, 81)), T.ToTensor(),
            T.Normalize([.485, .456, 0.406], [0.229, 0.224, 0.225])])
    else:
        raise NotImplementedError
    img = trans(img) if transform else img
    return img


class P2VNet(th.nn.Module):
    '''
    P2V Embedding Network
    '''
    def __init__(self):
        super(P2VNet, self).__init__()
        C = [1, 8, 16, 32]
        self.conv1 = th.nn.Conv2d(C[0], C[1], kernel_size=3, stride=3, padding=0)
        self.conv2 = th.nn.Conv2d(C[1], C[2], kernel_size=3, stride=3, padding=0)
        self.conv3 = th.nn.Conv2d(C[2], C[3], kernel_size=3, stride=3, padding=0)
        #self.conv4 = th.nn.Conv2d(64, 128, kernel_size=3, stride=3, padding=0, bias=False)

    def forward(self, image):
        b, c, h, w = image.shape
        ftm1 = th.nn.functional.relu(self.conv1(image))
        ftm2 = th.nn.functional.relu(self.conv2(ftm1))
        ftm3 = self.conv3(ftm2)

        ftm1 = th.nn.functional.interpolate(ftm1, size=[27, 27])
        ftm2 = th.nn.functional.interpolate(ftm2, size=[27, 27])
        ftm3 = th.nn.functional.interpolate(ftm3, size=[27, 27])
        #ftm1 = ftm1.repeat(1, 3, 3, 1).reshape(b, 16, h, w)
        #ftm2 = ftm2.repeat(1, 9, 9, 1).reshape(b, 32, h, w)
        #ftm3 = ftm3.repeat(1, 27, 27, 1).reshape(b, 64, h, w)

        ftm = th.cat((ftm1, ftm2, ftm3), dim=1)
        return ftm


class P2VLoss(th.nn.Module):
    def __init__(self):
        super(P2VLoss, self).__init__()
        self.CEL = th.nn.CosineEmbeddingLoss(margin=1.0, reduction='mean')

    def forward(self, p2v, labels):
        b, c, h, w = p2v.shape
        y = (labels[0::2]==labels[1::2]).float()*1 + (labels[0::2]!=labels[1::2]).float()*-1
        v1, v2 = p2v[0::2], p2v[1::2]
        #v1 = v1[:, random.randint(0, h-1), random.randint(0, w-1)]
        v1 = v1[:, 13, 13]
        #v2 = v2[:, random.randint(0, h-1), random.randint(0, w-1)]
        v2 = v2[:, 13, 13]
        cossim = 1 - th.nn.functional.pairwise_distance(v1, v2, p=2).detach().cpu().numpy()
        r = pearsonr(cossim, y.detach().cpu().numpy())
        return self.CEL(v1, v2, y), r


def train(model, crit, optim, images, labels):
    model.train()
    optim.zero_grad()
    p2v = model(images)
    loss, r = crit(p2v, labels)
    loss.backward()
    optim.step()
    return p2v, loss, r


def mainTrainMnist(argv):
    '''
    Train the model on Mnist
    '''
    ag = argparse.ArgumentParser()
    ag.add_argument('-D', '--device', default='cpu')
    ag.add_argument('--epoch', type=int, default=100)
    ag.add_argument('--batch', type=int, default=100)
    ag = ag.parse_args(argv)
    ag.device = th.device(ag.device)

    print('> Loading dataset')
    train_loader = th.utils.data.DataLoader(
            vision.datasets.MNIST(f'{os.getenv("HOME")}/.torch/mnist/', train=True, download=True,
                transform=vision.transforms.Compose([
                    vision.transforms.Resize((27, 27)),
                    vision.transforms.ToTensor(),
                    vision.transforms.Normalize((0.1307,), (0.3081,))
                    ])),
                batch_size=ag.batch, shuffle=True, num_workers=1, pin_memory=True)
    test_loader = th.utils.data.DataLoader(
            vision.datasets.MNIST(f'{os.getenv("HOME")}/.torch/mnist/', train=False,
                transform=vision.transforms.Compose([
                    vision.transforms.Resize((27, 27)),
                    vision.transforms.ToTensor(),
                    vision.transforms.Normalize((0.1307,), (0.3081,))
                ])),
                batch_size=ag.batch, shuffle=False, num_workers=1, pin_memory=True)

    print('> Create model')
    model = P2VNet().to(ag.device)
    crit = P2VLoss().to(ag.device)
    optim = th.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-7)

    loss0 = None
    for epoch in range(ag.epoch):
        for iteration, (images, labels) in enumerate(train_loader):
            images = images.to(ag.device)
            labels = labels.to(ag.device)
            p2v, loss, r = train(model, crit, optim, images, labels)
            if loss0 is None: loss0 = loss.item()
            #if iteration % 100==0:
            #    crit.visual(p2v[0].unsqueeze(0))

            print(f'Eph[{epoch}][{iteration}/{len(train_loader)}]',
                    f'p2v {p2v.shape},{p2v.var():.4f}',
                    f'loss {loss.item():.5f}',
                    f'loss/loss0 {loss.item()/loss0:.3f}',
                    f'r {r}',
                    sep='\t')


if __name__ == '__main__':
    eval(f'main{sys.argv[1]}')(sys.argv[2:])
