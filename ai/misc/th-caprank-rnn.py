'''
Image caption ranking -- using RNN

Pitfalls:
    1. outn, (hidn, cn) = lstm(emb, (0, 0))
       hidn is not the same with hidk (k=len(sent)), when the sent is padded
       and n neq k.

 - Score: max: 0.0328 min: -0.0273 mean: 0.0005 diag.mean: 0.0005
 - Recall(x->v)	@1: 24.4 (244),	@5: 55.6 (556),	@10: 70.0 (700),	
 - Recall(v->x)	@1: 15.2 (758),	@5: 43.2 (2161),	@10: 60.4 (3021),	
>> TRAIN @ Epoch 9

    2. The statistical property of the resulting RNN feature is quite bad.
       There are obvious horizontal or vertical stripes in the pcolor plot
       of the RNN features when the model is initialized by default method.
       When we change the LSTM weight initialization to N(0, 0.2), the stripes
       will disappear but the numberical values of the feature will be very
       large so that the sigmoid functions and tanh functions in LSTM are
       more likely to saturate. When the activation functions saturates,
       the resulting feature will have elements with large value. After
       p-2 normalizing, every element will turn into a very small value.
       The dot product of two vector representation is so small that the
       cosine distance is very short. Hence the inferior performance.

       FIXME: how to solve this?
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
import tqdm
import IPython

import torch as th
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from torch.utils.data.dataset import Subset
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import numpy as np
import pylab

from pairrankloss import PairRankLoss, recallAtk

def loadVocabMappings(vocab):
    vocab = pickle.load(vocab) # List[str]
    i2w = {i: w for i, w in enumerate(vocab)}
    w2i = {w: i for i, w in enumerate(vocab)}
    return i2w, w2i, len(vocab)

def cutLongSentences(toks, maxlen):
    for k, vs in toks.items():
        for i, v in enumerate(vs):
            toks[k][i] = v[:maxlen] if len(v)>maxlen else v
    return toks

def featstat(feat):
    return ' '.join([f'mean {feat.mean().data[0]:.5f}',
        f'var {feat.var().data[0]:.5f}', f'min {feat.min().data[0]:.5f}',
        f'max {feat.max().data[0]:.5f}'  ])

def makeVariable(tensor, use_cuda):
    if isinstance(tensor, np.ndarray):
        t = th.autograd.Variable(th.from_numpy(tensor), requires_grad=False)
    elif isinstance(tensor, th.Tensor):
        t = th.autograd.Variable(tensor, requires_grad=False)
    return t.cuda() if use_cuda else t.cpu()

class CocoDataset(Dataset):
    def __init__(self, cocoanno, cnnfeatpkl, tokspkl, vocab_w2i):
        self.json = json.load(cocoanno)
        self.cnnfeats = pickle.load(cnnfeatpkl)
        self.toks = cutLongSentences(pickle.load(tokspkl), 16)
        self.vocab_w2i = vocab_w2i
        ## get the max sequence length
        self.maxtoklen = 0
        for k, vs in self.toks.items():
            maxlen = max(map(len, vs))
            self.maxtoklen = maxlen if maxlen > self.maxtoklen else self.maxtoklen
        self.maxtoklen += 2 # for <start> and <end>
        self.maxtoklen = 18
        print('> max token sequence length', self.maxtoklen)
    def __len__(self):
        return len(self.json['images'])
    def __getitem__(self, index):
        imgid = self.json['images'][index]['id']
        # -- Get Image CNN feature, and duplicate 
        cnnfeat = self.cnnfeats[imgid]
        cnnfeat = np.repeat(cnnfeat, 5, axis=0)
        # -- Get tokens and translate
        itoks = np.ndarray((5, self.maxtoklen), dtype=np.int)
        itoks.fill(0)

        toks = self.toks[imgid]
        for i in range(5):
            itoks[i, 0] = self.vocab_w2i['<start>']
            for j, jw in enumerate(toks[i%len(toks)]):
                itoks[i, j+1] = self.vocab_w2i[jw]
            itoks[i, len(toks[i%len(toks)])+1] = self.vocab_w2i['<end>']

        #print(cnnfeat.shape, itoks.shape)
        return cnnfeat, itoks

class JEmbNet(th.nn.Module):
    def __init__(self, dvocab, dinput=300, dhid=512):
        super(JEmbNet, self).__init__()
        self.encoder = th.nn.Embedding(dvocab, dinput)
        self.rnn = th.nn.LSTM(dinput, dhid)
        self.cnntrans = th.nn.Linear(4096, 512)
        #self.cnnbn = th.nn.BatchNorm1d(512)
        #self.rnnbn = th.nn.BatchNorm1d(512)
        '''
        What?? BN leads to a worse statistical property of the scores?
        '''

    def forward(self, cnnfeat, toks):
        # [ cnn part ]
        assert(len(cnnfeat.shape) == 2)
        xs = th.nn.functional.relu(cnnfeat)
        xs = th.nn.functional.normalize(xs)
        xs = self.cnntrans(xs)
        #xs = self.cnnbn(xs)
        xs = th.nn.functional.relu(xs)
        xs = th.nn.functional.normalize(xs, dim=1) # MUST
        # [ rnn part ]
        assert(len(toks.shape) == 2)
        lens, idxs = th.sort((toks.data > 0).sum(1), descending=True)
        rmap = {v: i for i, v in enumerate(list(idxs))}
        ridx = [rmap[i] for i in range(toks.shape[0])] # used to restore order
        emb = self.encoder(toks[idxs].t())
        emb = th.nn.functional.normalize(emb, dim=2)  # norm input
        emb = pack_padded_sequence(emb, list(lens))
        out, (hn, cn) = self.rnn(emb)
        vs = hn.squeeze()[ridx]
        #vs = self.rnnbn(vs)
        vs = th.nn.functional.relu(vs)
        vs = th.nn.functional.normalize(vs, dim=1) # MUST

        ## [ another rnn part for verification ]
        #vvs = []
        #vlens = (toks.data > 0).sum(1)
        #for i in range(toks.shape[0]):
        #    v = toks[i,:vlens[i]].view(-1, 1)
        #    emb = self.encoder(v)
        #    emb = th.nn.functional.normalize(emb, dim=2)
        #    _, (hk, _) = self.rnn(emb)
        #    vvs.append(hk.squeeze())
        #vvs = th.stack(vvs)
        #vvs = th.nn.functional.normalize(vvs, dim=1)
        #print((vvs.detach() - vs.detach()).abs().sum().data[0])

        return xs, vs

def main_train():

    print('> Load Vocabulary')
    vocab_i2w, vocab_w2i, vocab_len = loadVocabMappings(ag.vocab)
    ag.vocab.close()
    print('  - vocab length', vocab_len)

    print('> initialize dataloader')
    rawtrainset = CocoDataset(ag.cocoanno, ag.cnnfeatpkl, ag.tokspkl, vocab_w2i)
    rawvalset = CocoDataset(ag.cocoannoval, ag.cnnfeatvalpkl, ag.toksvalpkl, vocab_w2i)
    trainset = ConcatDataset([rawtrainset, Subset(rawvalset, range(1000, len(rawvalset)))])
    valset = Subset(rawvalset, range(1000))
    print('  - training set size', len(trainset), 'val set size', len(valset))

    def mycollate(batch):
        xs, toks = zip(*batch)
        return np.vstack(xs), np.vstack(toks)
    trainloader = DataLoader(trainset, batch_size=32, num_workers=1,
            collate_fn=mycollate)

    print('> Create Model')
    model = JEmbNet(vocab_len)
    model = model.cuda() if ag.cuda else model.cpu()

    #th.nn.init.normal(model.rnn.weight_ih_l0, mean=0.0, std=0.02)
    #th.nn.init.uniform(model.rnn.weight_ih_l0, -0.2, 0.2)
    th.nn.init.normal(model.rnn.weight_hh_l0, mean=0.0, std=0.15)
    #th.nn.init.uniform(model.rnn.weight_hh_l0, -0.2, 0.2)
    #th.nn.init.eye(model.cnntrans.weight)
    #model.cnntrans.weight.data.add_(th.randn(512,512).cuda()*0.001)
    #th.nn.init.constant(model.rnn.bias_ih_l0, 0.2)
    #th.nn.init.constant(model.rnn.bias_hh_l0, 0.2)
    #th.nn.init.kaiming_uniform(model.rnn.weight_ih_l0)
    #th.nn.init.kaiming_uniform(model.rnn.weight_hh_l0)
    print(model)

    print('> Load glove vectors')
    if False:
        import torchtext as text
        glove = text.vocab.GloVe(name='6B', dim=300)
        notfound = 0
        vocabmiss = []
        for w, i in tqdm.tqdm(vocab_w2i.items()):
            if glove.stoi.get(w, False):
                # found, copy glove.vectors[j] to embeddings[i]
                j = glove.stoi.get(w)
                model.encoder.weight.data[i] = glove.vectors[j]
            else:
                #print(w, 'not found')
                notfound += 1
                vocabmiss.append(w)
        #model.encoder.weight.requires_grad = False
        print('> updated rnn.encoder with glove w2v')
        print(notfound, 'words not found')
        print(vocabmiss)
        del glove, notfound, vocabmiss

    print('> loss function and optimizer')
    crit = PairRankLoss(margin=0.2, metric='cosine')
    allparameters = [{'params': model.rnn.parameters()},
                     {'params': model.encoder.parameters(), 'lr':1e-5},
                {'params': model.cnntrans.parameters()}]
    optim = getattr(th.optim, ag.optim)(allparameters, lr=ag.lr, weight_decay=1e-7)

    print('> training loop ...')
    curve = {}
    for epoch in range(ag.maxepoch):

        # -- to through validation set
        if True:
            print('>> VALIDATION @Epoch', epoch)
            cnnfeats, rnnfeats = [], []
            model.eval()
            for iteration in tqdm.tqdm(range(1000)):
                xs, vs = valset[iteration]
                xs, vs = makeVariable(xs, ag.cuda), makeVariable(vs, ag.cuda)
                xs, vs = model(xs, vs)

                cnnfeats.append(xs.detach())
                rnnfeats.append(vs.detach())

            cnnfeats, rnnfeats = th.cat(cnnfeats), th.cat(rnnfeats)
            print('<> Dump CNN feats')
            print(featstat(cnnfeats))
            print('<> Dump RNN feats')
            print(featstat(rnnfeats))

            pylab.figure(); pylab.subplot(121)
            pylab.pcolormesh(cnnfeats.cpu().data.numpy(), cmap='cool');
            pylab.colorbar(); pylab.subplot(122)
            pylab.pcolormesh(rnnfeats.cpu().data.numpy(), cmap='cool');
            pylab.colorbar(); pylab.show()

            print('<> TEST RECALL')
            recallAtk(cnnfeats.cpu(), rnnfeats.cpu(), visual=True, reducerow=True)
            #recallAtk(cnnfeats.cpu(), rnnfeats.cpu(), visual=False, reducerow=True)
            #IPython.embed()
            del cnnfeats, rnnfeats

        # -- go through training set
        print('>> TRAIN @ Epoch', epoch)
        for iteration, (xs, toks) in enumerate(trainloader, 1):
            model.train()
            optim.zero_grad()

            xs, toks = makeVariable(xs, ag.cuda), makeVariable(toks, ag.cuda)
            #pylab.pcolormesh(xs.cpu().data.numpy()); pylab.show()
            #pylab.pcolormesh(toks.cpu().data.numpy()); pylab.show()
            xs, vs = model(xs, toks)

            loss = crit(xs, vs)
            loss.backward()
            th.nn.utils.clip_grad_norm(model.rnn.parameters(), 1e-1)
            th.nn.utils.clip_grad_norm(model.cnntrans.parameters(), 1e-1)
            optim.step()

            #pylab.pcolormesh(xs.cpu().data.numpy()); pylab.show()
            #pylab.pcolormesh(vs.cpu().data.numpy()); pylab.show()

            # [report]
            print('\033[32;1m - ', f'Epoch {epoch:d} / Iter {iteration:d}',
                    f'loss {loss.data[0]:.2f}', end='\033[m\n')

            #print(' -- cnnfeat stat', featstat(xs))
            #print(' -- rnnfeat stat', featstat(hidk))
            #if iteration % int(0.1*len(trainloader)) == 0:
            #    recallAtk(xs, vs, reducerow=True)
            #break
        #recallAtk(xs.cpu(), vs.cpu(), reducerow=True, visual=True)

def main_caprank():
    print('> Loading pre-trained rnn model')
    rnnmodel.load_state_dict(th.load(f'{__file__}.rnnmodel.final.{ag.maxiter}.pth'))
    CaptionGeneration(rnnmodel)

if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.set_defaults(func=ag.print_help)
    subag = ag.add_subparsers()
    # [train subparser]
    ag_train = subag.add_parser('train')
    ag_train.set_defaults(func=main_train)
    ag_train.add_argument('--cocoanno', type=argparse.FileType('r'),
            default='../coco/annotations/captions_train2014.json')
    ag_train.add_argument('--cocoannoval', type=argparse.FileType('r'),
            default='../coco/annotations/captions_val2014.json')
    ag_train.add_argument('--cnnfeatpkl', type=argparse.FileType('rb'),
            default='../coco-caption/coco.train.vgg19.v2.pkl')
    ag_train.add_argument('--cnnfeatvalpkl', type=argparse.FileType('rb'),
            default='../coco-caption/coco.val.vgg19.v2.pkl')
    ag_train.add_argument('--vocab', type=argparse.FileType('rb'),
            default='../coco-caption/buildvocab.py.vocab.pkl')
    ag_train.add_argument('--tokspkl', type=argparse.FileType('rb'),
            default='../coco-caption/buildvocab.py.toks.pkl')
    ag_train.add_argument('--toksvalpkl', type=argparse.FileType('rb'),
            default='../coco-caption/buildvocab.py.toksval.pkl')
    ag_train.add_argument('--lr', type=float, default=1e-5)
    ag_train.add_argument('--batch', type=int, default=37)
    ag_train.add_argument('--optim', type=str, default='Adam')
    ag_train.add_argument('--maxepoch', type=int, default=30)
#    ag_train.add_argument('--testevery', type=int, default=int(82783*1.0/25)) # 0.5 Epoch
    ag_train.add_argument('--rnn', type=str, default='LSTM')
    ag_train.add_argument('--cuda', default=False, action='store_true')
    # [caprank subparser]
    ag_caprank = subag.add_parser('caprank')
    ag_caprank.set_defaults(func=main_caprank)
    ag_caprank.add_argument('--cocopool', type=str, default='../coco/pool')
    # parse and dump
    ag = ag.parse_args()
    print('> Dump configuration')
    pprint(vars(ag))

    ag.func()
