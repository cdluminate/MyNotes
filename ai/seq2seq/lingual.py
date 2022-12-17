'''
Lingual Buildblocks for Machine Translation

Copyright (C) 2018 Mo Zhou
'''
import sys, os, re
import argparse
import pickle
from collections import Counter
import ujson as json
from pprint import pprint
from typing import *

import nltk
import tqdm
import joblib
import torch as th
from torch.utils.data import Dataset

sys.path.append('../')
from FlashLight import *


def europarlTokenize(fpath: str, *, partial:int = -1) -> (Dict, Counter):
    '''
    Tokenize all sentences in the given dataset.
    returns a Dict(id->sent), and a word counter.
    '''
    with open(fpath, 'r') as f:
        sentences = [line.strip() for line in f.readlines()]
        sentences = sentences[:partial] if partial > 0 else sentences
    tokens, wctr = dict(), Counter()

    # [serial version is slow]
    #for i, sent in tqdm.tqdm(enumerate(sentences), total=len(sentences)):
    #    tok = tokenize(sent)
    #    wctr.update(tok)
    #    tokens[i] = tok

    print('>', len(sentences), 'sentences to process')
    _tokens = joblib.Parallel(n_jobs=-1, verbose=5)(
            joblib.delayed(tokenize)(sent) for sent in sentences)
    print('>', 'word count')
    for tok in _tokens:
        wctr.update(tok)
    tokens = {int(k): v for (k, v) in enumerate(_tokens)}
    return tokens, wctr


def tokenFilter(tokens: Dict, vocab: Dict) -> Dict:
    '''
    Replace tokens that doesn't exist in the given vocabulary set with <unk>
    '''
    newtokens = {}
    sifter = lambda x: x if vocab.get(x, False) else '<unknown>'
    for sid, sent in tokens.items():
        newtokens[int(sid)] = list(map(sifter, sent))
    return newtokens


class MachineTransDataset(Dataset):
    '''
    Load corpus in source and destination language
    '''
    def __init__(self, src: str, dst: str, threshold: int = 5):
        print('> loading source language')
        srctokens, srcctr = jsonLoad(src)
        srcvocab = Vocabulary(srcctr, threshold)
        srctokens = tokenFilter(srctokens, srcvocab)
        print(' ', len(srctokens), 'vocab', len(srcvocab))
        print('> loading destination language')
        dsttokens, dstctr = jsonLoad(dst)
        dstvocab = Vocabulary(dstctr, threshold)
        dsttokens = tokenFilter(dsttokens, dstvocab)
        print(' ', len(dsttokens), 'vocab', len(dstvocab))
        assert(len(srctokens) == len(dsttokens))

        self.srctokens = srctokens
        self.dsttokens = dsttokens
        self.srcvocab = srcvocab
        self.dstvocab = dstvocab
    def __len__(self):
        return len(self.srctokens)
    def __getitem__(self, index):
        xid = index
        s, d = self.srctokens[xid], self.dsttokens[xid]
        s = ['<start>'] + s + ['<end>']
        d = ['<start>'] + d + ['<end>']
        s, d = self.srcvocab(s), self.dstvocab(d)
        return s, d, xid


if __name__ == '__main__':

    if sys.argv[1] == 'test':
        dataset = MachineTransDataset(sys.argv[2], sys.argv[3])
        print(dataset[0])
        for i in range(len(dataset)):
            src, dst, xid = dataset[i]
        exit()

    ag = argparse.ArgumentParser()

    ag.add_argument('--corpus', type=str)
    ag.add_argument('--saveto', type=str, default=f'{__file__}.toks.gz')
    ag.add_argument('--partial', type=int, default=-1)
    ag = ag.parse_args()
    pprint(vars(ag))

    tokens, ctr = europarlTokenize(ag.corpus, partial=ag.partial)
    print('saveto', ag.saveto)
    jsonSave([tokens, ctr], ag.saveto)

'''
>>> python3 lingual.py --corpus fr-en/europarl-v7.fr-en.en --saveto ep.en.toks.zst
>>> python3 lingual.py --corpus fr-en/europarl-v7.fr-en.fr --saveto ep.fr.toks.zst
'''
