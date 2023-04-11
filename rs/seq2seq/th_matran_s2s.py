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
# FIXME: [trick:original paper] reverse source language sequence.
# FIXME: is there any problem about initialization and LSTM weight initialization?
# FIXME: use tensorboardX
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

sys.path.append('../')
from FlashLight import *
import lingual


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
    elif isinstance(tensor, list) or isinstance(tensor, tuple):
        t = th.autograd.Variable(th.Tensor(tensor), requires_grad=False)
    else:
        raise TypeError
    return t.cpu() if not ag.cuda else t.cuda()


class SeqEncoder(th.nn.Module):
    '''
    Encode a input sequence with variable length into a fixed-size vector.
    '''
    def __init__(self, dsrcvocab, dimw2v=1000, dimhid=1000, layers=4):
        super(SeqEncoder, self).__init__()
        self.config = {'dimw2v': dimw2v, 'dimhid': dimhid, 'layers': layers}
        self.Emb = th.nn.Embedding(dsrcvocab, dimw2v)
        self.Rnn = th.nn.LSTM(dimw2v, dimhid, layers)

    def forward(self, itoks):
        # Sort
        paditoks, lens = padLLI(itoks)
        paditoks = makeVar(paditoks)
        sortidx = list(np.argsort(lens).flatten()[::-1])
        undoidx = [{v:i for i,v in enumerate(sortidx)}[i]
                   for i in range(len(lens))]
        # Forward
        emb = self.Emb(paditoks[sortidx, :].t())
        emb = pack_padded_sequence(emb, [lens[i] for i in sortidx])
        _, (hidn, _) = self.Rnn(emb)
        # Unsort
        hidn = hidn[:, undoidx, :]
        return hidn


class SeqDecoder(th.nn.Module):
    '''
    Decode a fixed-size input vector into a variable length sequence.
    '''
    def __init__(self, ddstvocab, dimw2v=1000, dimhid=1000, layers=4):
        super(SeqDecoder, self).__init__()
        self.config = {'dimw2v': dimw2v, 'dimhid': dimhid, 'layers': layers}
        self.Emb = th.nn.Embedding(ddstvocab, dimw2v)
        self.Rnn = th.nn.LSTM(dimw2v, dimhid, layers)
        self.Out = th.nn.Linear(dimhid, ddstvocab)
        self.Lsm = th.nn.LogSoftmax(dim=1)

    def forward(self, itoks, hid0):
        outn = []
        for i, itok in enumerate(itoks):
            itok = makeVar(itok).long().view(-1, 1)
            ihid0 = hid0[:, i, :].contiguous().view(
                self.config['layers'], 1, -1)
            emb = self.Emb(itok)
            emb = th.nn.functional.relu(emb)  # FIXME: Why do this ?
            outk, (_, _) = self.Rnn(emb, (ihid0, th.zeros(ihid0.shape).cuda()))
            distrib = self.Out(outk.squeeze())
            distrib = distrib.unsqueeze(0) if len(
                distrib.shape) == 1 else distrib
            distrib = self.Lsm(distrib)
            outn.append(distrib)
        outn = th.cat(outn, dim=0)
        return outn  # shape(sum_batch length, dvlen)

    def inference(self, itoks):
        raise NotImplementedError


def clAccuracy(distrib, target):
    '''
    distrib should be an (N, C) tensor. N for batchsize, C for num_class
    target should be a (N,) tensor.
    '''
    _, idxs = distrib.topk(k=1, dim=1)
    x = idxs.cpu().long().view(-1) == target.cpu().long().view(-1)
    return (x.sum().float() * 100. / target.numel()).data[0]


def getBLEU(distrib, target, lens, dset, dump=False):
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
    def _collate(batch):
        ss, ds, ids = zip(*batch)
        return ss, ds, ids

    print('> Load dataset')
    europarl = lingual.MachineTransDataset(ag.src, ag.dst)
    dataloader = DataLoader(europarl, ag.batch, num_workers=2,
            shuffle=True, collate_fn=_collate)

    print('> initialize encoder')
    encoder = SeqEncoder(len(europarl.srcvocab), ag.dimw2v, ag.dimhid, ag.layers)
    encoder = encoder.cuda() if ag.cuda else encoder

    print('> initialize decoder')
    decoder = SeqDecoder(len(europarl.dstvocab), ag.dimw2v, ag.dimhid, ag.layers)
    decoder = decoder.cuda() if ag.cuda else decoder

    print('> loss function')
    crit = th.nn.NLLLoss()

    print('> optimizer')
    all_params = [
        {'params': encoder.parameters()},
        {'params': decoder.parameters()},
    ]
    optim = th.optim.Adam(all_params, lr=ag.lr, weight_decay=1e-7)

    print('<> Start training')
    for epoch in range(ag.maxepoch):
        for i, (sv, dv, sids) in enumerate(dataloader):
            print(f'Eph [{epoch}][{i}/{len(dataloader)}]:')

            src_emb = encoder(sv)
            print(src_emb.shape)
            distrib = decoder([v[:-1] for v in dv], src_emb)

            expected = th.cat([makeVar(v[1:]) for v in dv], dim=0).long()
            loss = crit(distrib, expected)
            optim.zero_grad()
            loss.backward()
            optim.step()

            #bleu = getBLEU(distrib, expected,
            #    list(map(lambda x: len(x)-1, dv)), europarl, False)
            accu = clAccuracy(distrib, expected)
            print(' -', '\tloss', f'{loss.data[0]:.3f}',
                    '\taccu', f'{accu:.2f}')


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.set_defaults(func=ag.print_help)
    subag = ag.add_subparsers()

    # [ train subparser ]
    ag_train = subag.add_parser('train')
    ag_train.set_defaults(func=main_train)
    # -- I/O options
    ag_train.add_argument('--src', type=str)
    ag_train.add_argument('--dst', type=str)
    # -- optimization options
    ag_train.add_argument('--lr', type=float, default=2e-4)  # in paper: 2e-4
    ag_train.add_argument('--batch', type=int, default=128)  # in paper: 128
    ag_train.add_argument('--optim', type=str, default='Adam')
    ag_train.add_argument('--maxepoch', type=int, default=15)
    # -- model options
    ag_train.add_argument('--rnn', type=str, default='LSTM')  # in paper: LSTM
    ag_train.add_argument('--dimw2v', type=int, default=300)  # in paper: 1000
    ag_train.add_argument('--dimhid', type=int, default=512)  # in paper: 1000
    ag_train.add_argument('--layers', type=int, default=2)  # in paper: 4
    # -- misc
    ag_train.add_argument('--cuda', default=False, action='store_true')
    ag_train.add_argument('--session', type=str, default=f'sess.{time.time()}')

    # parse and dump
    ag = ag.parse_args()
    print('> Dump configuration')
    pprint(vars(ag))

    ag.func()
