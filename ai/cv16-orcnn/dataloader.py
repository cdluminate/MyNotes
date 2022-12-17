#!/usr/bin/env python3

import sys
import os
import numpy as np
import pandas as pd
import h5py
import pickle
import random
from multiprocessing import Process, Queue
from sklearn.model_selection import train_test_split

class DataLoader(object):
    def __init__(self):
        self.name = 'MORPH2 8/2'
        #self.h5path = '/niuz/dataset/morph2/morph2.cv16.wacv82.h5'
        self.h5path = '/niuz/dataset/morph2/morph2.wacv82.cv16.norotation.h5'
        print('=> Initializing {} DataLoader ...'.format(self.name))
        if not os.path.exists(self.h5path):
            self.create_hdf5()
        else:
            print('-> using Cached HDF5 ...')
        ### Cache all contents of HDF5 into Memory
        self.f = h5py.File(self.h5path, 'r')
        self.train_images = self.f['train/images'][:,:]
        self.train_labels = self.f['train/labels'][:,:]
        self.val_images = self.f['val/images'][:,:]
        self.val_labels = self.f['val/labels'][:,:]
        print(' -> train im shape', self.train_images.shape)
        print(' -> train lb shape', self.train_labels.shape)
        print(' -> val   im shape', self.val_images.shape)
        print(' -> val   lb shape', self.val_labels.shape)
        self.maxtrain = self.train_images.shape[0]
        self.maxval = self.val_images.shape[0]
        # Misc
        self.cur = {'train':0, 'val':0}
        self.max = {'train':self.maxtrain, 'val':self.maxval}
        print('=> Initializing {} DataLoader ... OK'.format(self.name))
    def reset(self, split):
        self.cur[split] = 0
    def inc(self, split):
        self.cur[split] += 1
    def itersInEpoch(self, split, batchsize):
        return int(self.max[split] / batchsize)
    def create_hdf5(self):
        return NotImplementedError("Use lang/py3/util.imageset.py to generate hdf5 instead")
    def getBatch(self, split, batchsize):
        '''
        split: str, {train, val}
        batchsize: int
        '''
        batchim = np.zeros((batchsize, 3, 64, 64))
        batchlb = np.zeros((batchsize, 1))
        batchids = []
        for i in range(batchsize):
            if self.cur[split] >= self.max[split]:
                self.reset(split)
            batchids.append(self.cur[split])
            self.inc(split)
        if split=='train':
            batchids = [ random.choice(range(self.maxtrain)) for _ in range(batchsize) ] # 75%->77%
            batchim[:,:] = self.train_images[batchids, :]
            batchlb[:,:] = self.train_labels[batchids, :]
        elif split=='val':
            batchim[:,:] = self.val_images[batchids, :]
            batchlb[:,:] = self.val_labels[batchids, :]
        else:
            raise Exception('Unexpected split')
        return batchim, batchlb

if __name__=='__main__':
    # test
    dataloader = DataLoader()
    images, labels = dataloader.getBatch('train', 1)
    print(type(images), type(labels))
    print(images, labels)
    for i in range(10000):
        print('get batch iter', i)
        images, labels = dataloader.getBatch('train', 64)
    print('test ok')
