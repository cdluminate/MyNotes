'''
Image Caption Ranking -- Two Branch Network
'''
import os
import sys
import argparse
import json
import pickle
from pprint import pprint

import numpy as np
import torch as th
from torch.utils.data import Dataset, DataLoader
import pylab

from pairrankloss import PairRankLoss


class trainingDataset(Dataset):
    def __init__(self, cocoanno, cnnfeatpkl, rnnfeatpkl):
        self.json = json.load(cocoanno)
        self.cnnfeats = pickle.load(cnnfeatpkl)
        self.rnnfeats = pickle.load(rnnfeatpkl)
    def __len__(self):
        return len(self.json['images'])
    def __getitem__(self, index):
        fname = self.json['images'][index]['file_name']
        imgid = self.json['images'][index]['id']
        rnnfeat = self.rnnfeats[imgid]
        rnnfeat = np.vstack([rnnfeat[i%len(rnnfeat)] for i in range(5)])
        #cnnfeat = np.load(os.path.join(self.cnnfeatpool, fname + '.cnnfeat.npz'))['arr_0']
        cnnfeat = self.cnnfeats[imgid]
        cnnfeat = np.vstack([cnnfeat for _ in range(5)])
        #print(cnnfeat.shape, rnnfeat.shape)
        return cnnfeat, rnnfeat

class TwoBranchNet(th.nn.Module):
    '''
    two-branch-net implementation
    '''
    def __init__(self, dcnnfeat, drnnfeat, demb):
        super(TwoBranchNet, self).__init__()

        self.dcnnfeat = dcnnfeat
        self.drnnfeat = drnnfeat
        self.dcnnhid  = 512
        self.drnnhid  = 512
        self.demb     = demb

        # [cnn/vision branch]
        self.xlinear1 = th.nn.Linear(self.dcnnfeat, self.dcnnhid)
        self.xlinear2 = th.nn.Linear(self.dcnnhid, self.demb)
        self.xbn      = th.nn.BatchNorm1d(self.demb)

        # [rnn/language branch]
        self.vlinear1 = th.nn.Linear(self.drnnfeat, self.drnnhid)
        self.vlinear2 = th.nn.Linear(self.drnnhid, self.demb)
        self.vbn      = th.nn.BatchNorm1d(self.demb)

    def forward(self, x, v):
        '''
        x for image feature batch, y for sentence feature batch.
        size of x is (batch, feature dim).
        size of y is (batch, feature dim).
        '''
        x = self.xlinear1(x)
        x = th.nn.functional.relu(x)
        x = self.xlinear2(x)
        x = self.xbn(x)
        x = th.nn.functional.normalize(x)

        v = self.vlinear1(v)
        v = th.nn.functional.relu(v)
        v = self.vlinear2(v)
        v = self.vbn(v)
        v = th.nn.functional.normalize(v)

        return x, v


def main_train():

    print('> load training dataset')
    trainingdataset = trainingDataset(ag.cocoanno, ag.cnnfeatpkl, ag.rnnfeatpkl)
    def mycollate(batch):
        xs, vs = zip(*batch)
        return np.vstack(xs), np.vstack(vs)
    trainingloader = DataLoader(trainingdataset, batch_size=37, num_workers=1,
            collate_fn=mycollate)

    print('> create two branch net')
    twobnet = TwoBranchNet(4096, 512, 512)
    twobnet = twobnet.cuda() if ag.cuda else twobnet.cpu()
    print(twobnet)

    print('> criterion and optim')
    crit = PairRankLoss(margin=0.2, metric='cosine')
    optim = getattr(th.optim, ag.optim)(twobnet.parameters(), lr=1e-3, weight_decay=1e-7)

    print('> training')
    for epoch in range(1, ag.maxepoch+1):
        twobnet.train()
        for iteration, (xs, vs) in enumerate(trainingloader, 1):
            # get batch
            xs = th.autograd.Variable(th.from_numpy(xs), requires_grad=False)
            vs = th.autograd.Variable(th.from_numpy(vs), requires_grad=False)
            xs, vs = (xs.cuda(), vs.cuda()) if ag.cuda else (xs, vs)
            # forward
            xs, vs = twobnet(xs, vs)
            loss = crit(xs, vs)
            if iteration % 10 == 0: recallK(xs, vs)
            print(f'> Iter {epoch}/{iteration}', f'\tloss {loss.data[0]:.2f}')
            # backward & update
            optim.zero_grad()
            loss.backward()
            optim.step()
            if iteration == 10: break
        recallK(xs, vs, visual=True)
    recallK(xs, vs, visual=True)


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.set_defaults(func=ag.print_help)
    subag = ag.add_subparsers()
    # [ arguments for training ]
    ag_train = subag.add_parser('train')
    ag_train.add_argument('--cocoanno', type=argparse.FileType('r'),
            default='../coco/annotations/captions_train2014.json')
    ag_train.add_argument('--cocoannoval', type=argparse.FileType('r'),
            default='../coco/annotations/captions_val2014.json')
    ag_train.add_argument('--cnnfeatpkl', type=argparse.FileType('rb'),
            default='../coco-caption/coco.train.vgg19.tencrop.cnnfeats.pkl')
    ag_train.add_argument('--rnnfeatpkl', type=argparse.FileType('rb'),
            default='../coco-caption/th-capgen.py.sentfeats.pkl')
    ag_train.add_argument('--lr', type=float, default=1e-3)
    ag_train.add_argument('--optim', type=str, default='Adam', choices=['Adam'])
    ag_train.add_argument('--maxepoch', type=int, default=30)
    ag_train.add_argument('--cuda', default=False, action='store_true')
    ag_train.set_defaults(func=main_train)
    # [ ... ]
    ag = ag.parse_args()
    print('> dump configurations')
    pprint(vars(ag))
    ag.func()
