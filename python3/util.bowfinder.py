#!/usr/bin/python3
'''
BoW-based Line finder
TODO: change binarized bow representation to formal bow representation
TODO: another fuzzy search method is to expand "keyword" to ".*k.*e.*y.*w......"
'''
import os
import sys
import argparse
from typing import *
import numpy as np


def getVocabulary(lines: List[str]) -> Dict[Any,Any]:
    '''
    Get a vocabulary set from the given strings. No uppercase alphabets.
    '''
    vset = set()
    for line in (x.lower().split() for x in lines):
        vset.update(line)
    vlist = list(sorted(vset))
    d = {int(k): str(v) for (k, v) in enumerate(vlist)}
    d.update({str(v): int(k) for (k, v) in enumerate(vlist)})
    return d  # bi-directional dictionary


def line2bow(line: str, vocab: dict) -> np.ndarray:
    '''
    convert a line into a (binary) BoW representation.
    The last place is reserved for the <Unknown> token.
    '''
    bow = np.zeros(1 + len(vocab)//2, dtype=np.uint8)
    idx = [vocab.get(x, len(vocab)//2) for x in line.lower().split()]
    bow[idx] = 1
    return bow


def lines2bow(lines: List[str], vocab: dict) -> np.ndarray:
    '''
    convert a list of lines into a single ndarray.
    '''
    bows = np.zeros((len(lines), 1+len(vocab)//2), dtype=np.uint8)
    for i, line in enumerate(lines):
        bows[i] = line2bow(line, vocab)
    return bows


def searchLine(lines: List[str], query: str,
               *, topk=10) -> np.ndarray:
    '''
    find the top-k matching lines
    '''
    vocab = getVocabulary(lines + [query])
    print('=> vocabulary length', len(vocab))
    bows = lines2bow(lines, vocab)  # (lines, vocabsize)
    qbow = line2bow(query, vocab)  # (vocabsize,)
    #print(bows.shape, qbow.shape)
    scores = np.matmul(bows, qbow) # (lines,)
    idx = np.argmax(scores).flatten()[::-1][:topk]  # descending
    #print(scores.argmax().flatten())
    return idx


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('-f', '--file', type=str, required=True)
    ag.add_argument('-n', '--needle', type=str, required=True)
    ag.add_argument('-k', '--topk', type=int, default=10)
    ag.add_argument('-m', '--method', type=str, default='bow')
    ag = ag.parse_args()
    print(ag)

    with open(ag.file, 'r') as f:
        lines = f.readlines()
    idx = searchLine(lines, ag.needle, topk=3)
    for nl, line in [(x+1, lines[x]) for x in idx]:
        print(nl, '->', repr(line))
