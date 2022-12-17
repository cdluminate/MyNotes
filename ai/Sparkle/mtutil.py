'''
FlashLight: Personal PyTorch Helpers
Copyright (C) 2018 Mo Zhou
'''
from typing import *
import re
import nltk
import numpy as np
import string


def tokenize(s: str) -> List[str]:
    '''
    Turn a raw sentence into a list of tokens.
    '''
    tok = re.sub(f'[{string.punctuation}]', ' ', s)  # remove punctuation
    tok = ' '.join(tok.lower().split())  # lower and reformat
    tok = nltk.word_tokenize(tok)  # tokenize
    return tok


def padLLI(lli: List[List[int]], padding=0) -> (List[List[int]], List[int]):
    '''
    Pad a list of lists of integers with zero. The lenghts of lists may vary.
    a numpy.array with shape (num_lists, maxlen) will be returned.
    '''
    lens = list(map(len, lli))
    paddedlli = []
    for j, li in enumerate(lli):
        paddedlli.append(list(lli[j]) + [padding] * (max(lens) - len(li)))
    return paddedlli, lens


def npadLLI(lli, padding=0):
    padded, lens = padLLI(lli, padding)
    return np.array(padded), lens



def test_padlli():
    orig = [[1,2,3], [1,2]]
    target, targetlens = [[1,2,3], [1,2,0]], [3,2]
    padded, lens = padLLI(orig)
    assert(target == padded)
    assert(targetlens == lens)


def test_npadlli():
    orig = [[1,2,3], [1,2]]
    target, targetlens = [[1,2,3], [1,2,0]], [3,2]
    padded, lens = npadLLI(orig)
    assert(np.power(padded - np.array(target), 2).sum() < 1e-9)
    assert(targetlens == lens)
