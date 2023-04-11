'''
FlashLight: Personal PyTorch Helpers
'''
from typing import *
import sys
import os
import re
import _io
import pickle
import ujson as json  # Fastest Json
from collections import Counter, defaultdict
import string
from pprint import pprint
import gzip
import zstd
import unittest

import nltk
import numpy as np
import torch as th


class Vocabulary(object):
    '''
    Load vocabulary from word counter, and do the i->w / w->i mapping
    '''

    def __init__(self, ctr: Counter, threshold=5):
        self.vocab = {}
        self.vocablist = ['<padding>', '<start>',
                          '<end>', '<unknown>']  # 0 1 2 3
        self.vocablist.extend(
            sorted(k for k, v in ctr.items() if v >= threshold))
        for (i, w) in enumerate(self.vocablist):
            self.vocab[int(i)] = str(w)
            self.vocab[str(w)] = int(i)
        self.threshold = threshold

    def __len__(self):
        return len(self.vocablist)

    def __repr__(self):
        return f'Vocabulary(size={len(self)})'

    def __getitem__(self, index):
        if isinstance(index, list):
            return [self.__getitem__(x) for x in index]
        elif isinstance(index, str):
            return self.vocab.get(index, 3)  # <unknown>
        elif isinstance(index, int):
            return self.vocab.get(index, '<unknown>')
        else:
            raise TypeError(f"{type(index)}: {index}")

    def __call__(self, index):
        return self.__getitem__(index)

    def get(self, index, fallback):
        '''
        FIXME: we really need this?
        '''
        return self.vocab.get(index, fallback)


def test_vocabulary_len():
    ctr = Counter(['test', 'test', 'vocab', 'torch'])
    vocab = Vocabulary(ctr, threshold=5)
    assert(4 == len(vocab))
    vocab = Vocabulary(ctr, threshold=0)
    assert(7 == len(vocab))


def test_vocabulary_getitem_bystr():
    ctr = Counter(['arbitrary', 'beef', 'candle'])
    vocab = Vocabulary(ctr, threshold=0)
    assert(0 == vocab['<padding>'])
    assert(1 == vocab['<start>'])
    assert(2 == vocab['<end>'])
    assert(3 == vocab['<unknown>'])
    assert(4 == vocab['arbitrary'])
    assert(5 == vocab['beef'])
    assert(6 == vocab['candle'])
    assert(3 == vocab['no such word'])


def test_vocabulary_getitem_byint():
    ctr = Counter(['arbitrary', 'beef', 'candle'])
    vocab = Vocabulary(ctr, threshold=0)
    assert('<padding>' == vocab[0])
    assert('<start>' == vocab[1])
    assert('<end>' == vocab[2])
    assert('<unknown>' == vocab[3])
    assert('candle' == vocab[6])
    assert('<unknown>' == vocab[999])


def test_vocabulary_getitem_bylist():
    ctr = Counter(['arbitrary', 'beef', 'candle'])
    vocab = Vocabulary(ctr, threshold=0)
    assert([0, 3, 6] == vocab[['<padding>', '<unknown>', 'candle']])
    assert(['<padding>', '<unknown>', 'candle'] == vocab[[0, 3, 6]])
