'''
PyTorch Seq2Seq / Machine Translation

Orignal Seq2seq paper
----------------------
https://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf

Other references
----------------
http://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html

Discussion
----------
# FIXME: bidirectional, GRU, teacher-enforcing
# FIXME: how does seq2seq utilize these hidden states?
# FIXME: pack sequences to boost speed?
# FIXME: [trick:original paper] reverse source language sequence.
# FIXME: is there any problem about initialization and LSTM weight initialization?
'''
import pickle
import json
import sys
import os
import argparse
import pickle
from pprint import pprint
from functools import reduce
import random
from subprocess import call
from typing import *
import time
from statistics import mean

import torch as th
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pack_padded_sequence
import numpy as np
from nltk.translate.bleu_score import sentence_bleu

import tensorboard_logger as tbl


def loadVocabMappings(vocab):
    '''
    Create two dictionaries that map between word and index.
    @in vocab: a list including all valid vocabularies(str)
    '''
    i2w = {i: w for i, w in enumerate(vocab)}
    w2i = {w: i for i, w in enumerate(vocab)}
    return i2w, w2i, len(vocab)


def padLLI(lli: List[List[int]], padding = 0) -> np.array:
    '''
    Pad a list of lists of integers with zero. The lenghts of lists may vary.
    a numpy.array with shape (num_lists, maxlen) will be returned.
    '''
    maxlen = max(map(len, lli))
    pdli = []
    for j, li in enumerate(lli):
        pdli.append( list(lli[j]) + [padding] * (maxlen - len(li)) )
    return np.array(pdli)


def breakLine(line, lens):
    '''
    break a long line into piecies according to lens
    '''
    assert(len(line) == sum(lens))
    lines, cursor = [], 0
    for l in lens:
        lines.append(line[cursor:cursor+l])
        cursor += l
    return lines


def makeVar(tensor):
    if isinstance(tensor, np.ndarray):
        t = th.autograd.Variable(th.from_numpy(tensor), requires_grad=False)
    elif isinstance(tensor, th.Tensor):
        t = th.autograd.Variable(tensor, requires_grad=False)
    elif isinstance(tensor, list):
        t = th.autograd.Variable(th.Tensor(tensor), requires_grad=False)
    elif isinstance(tensor, tuple):
        t = th.autograd.Variable(th.zeros(*tensor), requires_grad=False)
    else:
        raise TypeError
    return t.cpu() if not ag.cuda else t.cuda()


class MTDataset(Dataset):
    def __init__(self, srctoks, srcvocab, dsttoks, dstvocab):
        self.srctoks = pickle.load(srctoks)
        self.dsttoks = pickle.load(dsttoks)
        assert(len(self.srctoks) == len(self.dsttoks))
        si2w, sw2i, svlen = loadVocabMappings(pickle.load(srcvocab))
        di2w, dw2i, dvlen = loadVocabMappings(pickle.load(dstvocab))
        self.sw2i, self.svlen, self.si2w = sw2i, svlen, si2w
        self.dw2i, self.dvlen, self.di2w = dw2i, dvlen, di2w
        print(f' - dataset size {len(self.srctoks)}')
        print(f' - src vocab {svlen}, dst vocab {dvlen}')
        print(' -', sw2i['<start>'], sw2i['<unknown>'], sw2i['<end>'], sw2i['<padding>'])
        print(' -', dw2i['<start>'], dw2i['<unknown>'], dw2i['<end>'], dw2i['<padding>'])

    def __len__(self):
        return len(self.srctoks)

    def __getitem__(self, index):
        stok = ['<start>'] + self.srctoks[index] + ['<end>']
        dtok = ['<start>'] + self.dsttoks[index] + ['<end>']
        stok = list(map(lambda x: self.sw2i.get(x, -1), stok))
        dtok = list(map(lambda x: self.dw2i.get(x, -1), dtok))
        return stok, dtok

    def drestore(self, itoks):
        '''
        restore toks from itoks by using destination vocabulary
        '''
        toks = list(map(lambda x: self.di2w.get(x, '???'), itoks))
        return toks

    @staticmethod
    def getLoader(dataset, batch=128):
        def collatefunction(batch):
            sv, dv = zip(*batch)
            return sv, dv
        return DataLoader(dataset, batch, num_workers=1,
                          collate_fn=collatefunction)


class SeqEncoder(th.nn.Module):
    '''
    Encode a input sequence with variable length into a fixed-size vector.
    '''

    def __init__(self, dsrcvocab, dw2v=1000, dhid=1000, layers=4):
        '''
        @in dsrcvocab: source language vocabulary size
        @in dw2v: dimension of word2vec
        @in dhid: dimension of hidden state and memory cell if applicable
        @in layers: number of layers of the RNN
        '''
        super(SeqEncoder, self).__init__()
        self.config = {'dw2v': dw2v, 'dhid': dhid, 'layers': layers}
        self.Emb = th.nn.Embedding(dsrcvocab, dw2v)
        self.Rnn = th.nn.LSTM(dw2v, dhid, layers)

    def forward(self, itoks):
        '''
        @in itoks: a batch of indexes of tokenized sentence
        '''

        # [ forward one by one, very slow ]
        #hidn = []
        #for i, itok in enumerate(itoks):
        #    itok = makeVar(itok).long().view(-1, 1)
        #    emb = self.Emb(itok)
        #    _, (hidk, _) = self.Rnn(emb)
        #    hidn.append(hidk)  # multi-layer
        #hidn = th.cat(hidn, dim=1)

        # [ batch forward in parallel, fast ]
        paditoks = makeVar(padLLI(itoks))
        lens, idxs = th.sort((paditoks > 0).sum(1), descending=True)
        rmap = {v: i for i, v in enumerate(list(idxs.cpu().data))}
        ridx = [rmap[i] for i in range(len(itoks))]
        emb = self.Emb(paditoks[idxs].t())
        emb = pack_padded_sequence(emb, list(lens.cpu().data))
        _, (hidn, _) = self.Rnn(emb)
        assert(len(hidn.squeeze().shape) == 3)
        hidn = hidn.squeeze()[:, ridx, :]

        #print(hidn.shape)
        return hidn  # shape(batch, dhid)

    def inference(self, itoks):
        raise NotImplementedError


class SeqDecoder(th.nn.Module):
    '''
    Decode a fixed-size input vector into a variable length sequence.
    '''

    def __init__(self, ddstvocab, dw2v=1000, dhid=1000, layers=4):
        '''
        @in ddstvocab: vocabulary size of destination language
        '''
        super(SeqDecoder, self).__init__()
        self.config = {'dw2v': dw2v, 'dhid': dhid, 'layers': layers}
        self.Emb = th.nn.Embedding(ddstvocab, dw2v)
        self.Rnn = th.nn.LSTM(dw2v, dhid, layers)
        self.Out = th.nn.Linear(dhid, ddstvocab)
        self.Lsm = th.nn.LogSoftmax(dim=1)

    def forward(self, itoks, hid0):
        '''
        @in itoks: list of lists containing digital target sentence
        @in hid0: encoded source sequence vector
        '''
        outn = []
        for i, itok in enumerate(itoks):
            itok = makeVar(itok).long().view(-1, 1)
            ihid0 = hid0[:, i, :].contiguous().view(
                self.config['layers'], 1, -1)
            emb = self.Emb(itok)
            emb = th.nn.functional.relu(emb)  # FIXME: Why do this ?
            outk, (_, _) = self.Rnn(emb, (ihid0, makeVar((ihid0.shape))))
            distrib = self.Out(outk.squeeze())
            distrib = distrib.unsqueeze(0) if len(
                distrib.shape) == 1 else distrib
            distrib = self.Lsm(distrib)
            outn.append(distrib)
        outn = th.cat(outn, dim=0)
        return outn  # shape(sum_batch length, dvlen)


def clAccuracy(distrib, target):
    '''
    distrib should be an (N, C) tensor. N for batchsize, C for num_class
    target should be a (N,) tensor.
    '''
    _, idxs = distrib.topk(k=1, dim=1)
    x = idxs.cpu().long().view(-1) == target.cpu().long().view(-1)
    return (x.sum().float() * 100. / target.numel()).data[0]


def mtBLEU(distrib, target, lens, dset, dump=False):
    '''
    calculate the BLEU score.
    optionally dump the reference and candidate sentences.
    target should be the target sentence

    https://machinelearningmastery.com/calculate-bleu-score-for-text-python/
    '''
    _, idxs = distrib.topk(k=1, dim=1)
    assert(sum(lens) == target.numel() == idxs.numel())
    idxs = idxs.view(-1).cpu().data.numpy()
    target = target.view(-1).cpu().data.numpy()
    candidates = breakLine(dset.drestore(list(idxs)), lens)
    references = breakLine(dset.drestore(list(target)), lens)
    scores = []
    for can, ref in zip(candidates, references):
        if dump: print('  ', 'Candidate', can, '|', 'GT', ref)
        bleu = sentence_bleu([ref], can)
        scores.append(bleu)
    return mean(scores)


def main_train():
    '''
    Train a Machine Translation Model in the Seq2Seq Manner
    '''

    print('> Load dataset')
    europarl = MTDataset(ag.srctoks, ag.srcvocab, ag.dsttoks, ag.dstvocab)
    dataloader = MTDataset.getLoader(europarl, ag.batch)

    print('> initialize encoder')
    encoder = SeqEncoder(europarl.svlen, ag.dw2v, ag.dhid, ag.layers)
    encoder = encoder.cuda() if ag.cuda else encoder

    print('> initialize decoder')
    decoder = SeqDecoder(europarl.dvlen, ag.dw2v, ag.dhid, ag.layers)
    decoder = decoder.cuda() if ag.cuda else decoder

    print('> loss function')
    crit = th.nn.NLLLoss()

    print('> optimizer')
    all_params = [
        {'params': encoder.parameters()},
        {'params': decoder.parameters()},
    ]
    optim = th.optim.Adam(all_params, lr=ag.lr, weight_decay=1e-7)

    print('> logger')
    tbl.configure(ag.session, flush_secs=5)

    print('<> Start training')
    for epoch in range(ag.maxepoch):
        for i, (sv, dv) in enumerate(dataloader):
            print(f'> Eph [{epoch}][{i}/{len(dataloader)}]')
            src_emb = encoder(sv)
            distrib = decoder([v[:-1] for v in dv], src_emb)
            expected = th.cat([makeVar(v[1:]) for v in dv], dim=0).long()
            loss = crit(distrib, expected)
            optim.zero_grad()
            loss.backward()
            optim.step()

            bleu = mtBLEU(distrib, expected,
                list(map(lambda x: len(x)-1, dv)), europarl, False)
            accu = clAccuracy(distrib, expected)
            print(' -', '\tloss', f'{loss.data[0]:.3f}',
                    '\taccu', f'{accu:.2f}', '\tBLEU', f'{bleu:.2f}')
            tbl.log_value('class loss', loss.data[0],
                    step = i + epoch * len(dataloader))
            tbl.log_value('class accuraccy', clAccuracy(distrib, expected),
                    step = i + epoch * len(dataloader))
            tbl.log_value('BLEU', bleu,
                    step = i + epoch * len(dataloader))


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.set_defaults(func=ag.print_help)
    subag = ag.add_subparsers()

    # [ train subparser ]
    ag_train = subag.add_parser('train')
    ag_train.set_defaults(func=main_train)
    # -- I/O options
    ag_train.add_argument('--srctoks', type=argparse.FileType('rb'),
                          default='../seq2seq/buildvocab.py.src.toks.pkl')
    ag_train.add_argument('--dsttoks', type=argparse.FileType('rb'),
                          default='../seq2seq/buildvocab.py.dst.toks.pkl')
    ag_train.add_argument('--srcvocab', type=argparse.FileType('rb'),
                          default='../seq2seq/buildvocab.py.src.vocab.pkl')
    ag_train.add_argument('--dstvocab', type=argparse.FileType('rb'),
                          default='../seq2seq/buildvocab.py.dst.vocab.pkl')
    # -- optimization options
    ag_train.add_argument('--lr', type=float, default=2e-4)  # in paper: 2e-4
    ag_train.add_argument('--batch', type=int, default=16)  # in paper: 128
    ag_train.add_argument('--optim', type=str, default='Adam')
    ag_train.add_argument('--maxepoch', type=int, default=15)
    # -- model options
    ag_train.add_argument('--rnn', type=str, default='LSTM')  # in paper: LSTM
    ag_train.add_argument('--dw2v', type=int, default=300)  # in paper: 1000
    ag_train.add_argument('--dhid', type=int, default=512)  # in paper: 1000
    ag_train.add_argument('--layers', type=int, default=2)  # in paper: 4
    # -- misc
    ag_train.add_argument('--cuda', default=False, action='store_true')
    ag_train.add_argument('--session', type=str, default=f'sess.{time.time()}')

    # parse and dump
    ag = ag.parse_args()
    print('> Dump configuration')
    pprint(vars(ag))

    ag.func()
