'''
Image caption generation

[Resnet18 (10 crop) + Single direction LSTM]
   4 epoches @LOW-OVERFIT
   ~7 epoches @BEST-HUMANEVAL

Note, the model aims to learn a distribution P(x_t|x_{t-1}=..., h_0=cnnfeat).
The model accepts zero initial hidden state, but the behaviour and output
quality is not guaranteed.
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

import torch as th
import numpy as np

def vocabmappings(vocabpath):
    with open(vocabpath, 'rb') as f:
        vocab = pickle.load(f) # list[str]
    i2w = {i: w for i, w in enumerate(vocab)}
    w2i = {w: i for i, w in enumerate(vocab)}
    return i2w, w2i, len(vocab)

def transi2w(xs):
    return list(map(lambda x: vocab_i2w[x], xs))

def Ltransi2w(lxs):
    return list(map(transi2w, lxs))

def transw2i(ws):
    return list(map(lambda w: vocab_w2i.get(w, vocab_w2i['<unknown>']), ws))

def Ltransw2i(lws):
    return list(map(transw2i, lws))

def Ltransi2n(lxs):
    ns = reduce(list.__add__, lxs)
    return ns

def Ltransn2w(lxs):
    ws = [transi2w(xs) for xs in lxs]
    for i in range(len(ws)):
        specialwords = ['<padding>', '<start>', '<end>']
        ws[i] = ' '.join(list(filter(lambda x: x not in specialwords, ws[i])))
    return ws

class DataLoader(object):
    def __init__(self, cocoanno=ag.cocoanno, toks=ag.toks,
            batch=ag.batch, featpool=ag.featpool):
        with open(cocoanno, 'r') as f:
            self.json_orig = json.load(f)
        with open(toks, 'rb') as f:
            self.toks = pickle.load(f)
        self.batch = batch
        self.featpool = featpool
        self.loc = 0
    def __len__(self):
        return len(self.json_orig['images'])
    def getBatch(self):
        #images_j = self.json_orig['images'][:self.batch]
        images_j = random.choices(self.json_orig['images'], k=self.batch)
        # -- retrieve tokens and translate
        #tokensBatch = [random.choices(self.toks[img['id']], k=5) for img in images_j]
        tokensBatch = [self.toks[img['id']] for img in images_j]
        lens = list(map(len, tokensBatch))
        tokensBatch = [Ltransw2i(tokens) for tokens in tokensBatch]
        tokensBatch = Ltransi2n(tokensBatch)
        maxlen = max(map(len, tokensBatch)) + 2
        nptokensBatch = np.ndarray((len(tokensBatch), maxlen), dtype=np.int)
        nptokensBatch.fill(0)
        for i, iv in enumerate(tokensBatch):
            nptokensBatch[i, 0] = vocab_w2i['<start>']
            for j, jw in enumerate(iv):
                nptokensBatch[i, j+1] = jw
            nptokensBatch[i, len(iv)+1] = vocab_w2i['<end>']
        tokensBatch = nptokensBatch
        # -- retrieve cnn features
        imagesBatch = [os.path.join(ag.featpool, im['file_name']+'.cnnfeat.npz')
                for im in images_j]
        imagesBatch = [np.load(im)['arr_0'] for im in imagesBatch]
        imagesBatch = reduce(list.__add__, [[x for _ in range(lens[i])] for (i, x) in enumerate(imagesBatch)]) # duplicate
        #imagesBatch = np.concatenate(imagesBatch).reshape(len(imagesBatch), -1)
        imagesBatch = np.vstack(imagesBatch).reshape(len(imagesBatch), -1)

        #print('im', imagesBatch.shape, 'lb', tokensBatch.shape)
        #imagesBatch = th.autograd.Variable(th.from_numpy(imagesBatch), requires_grad=False)
        #tokensBatch = th.autograd.Variable(th.from_numpy(tokensBatch), requires_grad=False)
        return imagesBatch, tokensBatch

class DataLoaderVal(object):
    def __init__(self, cocoanno=ag.cocoannoval, toks=ag.toksval,
            batch=ag.batch, featpool=ag.featpool):
        with open(cocoanno, 'r') as f:
            self.json_orig = json.load(f)
        with open(toks, 'rb') as f:
            self.toks = pickle.load(f)
        self.batch = batch
        self.featpool = featpool
    def __len__(self):
        return len(self.json_orig['images'])
    def __getitem__(self, index):
        image_idx = self.json_orig['images'][index]
        # tokens
        tokB = self.toks[image_idx['id']]
        tokB = Ltransw2i(tokB)
        maxlen = max(map(len, tokB)) + 2
        ntokB = np.ndarray((len(tokB), maxlen), dtype=np.int)
        ntokB.fill(0)
        for i, iv in enumerate(tokB):
            ntokB[i, 0] = vocab_w2i['<start>']
            for j, jw in enumerate(iv):
                ntokB[i, j+1] = jw
            ntokB[i, len(iv)+1] = vocab_w2i['<end>']
        # image
        imgB = [os.path.join(ag.featpool, image_idx['file_name']+'.cnnfeat.npz')]
        imgB = [np.load(im)['arr_0'] for im in imgB]
        imgB = reduce(list.__add__, [[x for _ in range(len(tokB))] for x in imgB]) # duplicate
        imgB = np.vstack(imgB).reshape(len(imgB), -1)
        return imgB, ntokB

class RNNmodel(th.nn.Module):
    def __init__(self, dvocab, rnn_type=ag.rnn, nonlinearity='tanh',
            dinput=256, dhid=512, layers=1, dropout=0.0):
        super(RNNmodel, self).__init__()
        self.drop = th.nn.Dropout(dropout)
        self.encoder = th.nn.Embedding(dvocab, dinput, padding_idx=0)
        #self.rnn = th.nn.RNN(dinput, dhid, layers,
        #        nonlinearity=nonlinearity, dropout=dropout)
        self.rnn = getattr(th.nn, rnn_type)(
                dinput, dhid, layers, dropout=dropout)
        self.decoder = th.nn.Linear(dhid, dvocab)

        if ag.cnndimreduc:
            self.dimreduc = th.nn.Sequential()
            self.dimreduc.add_module('cnn_dim_reduc', th.nn.Linear(4096, 512))

    def forward(self, inp, hid0):
        if ag.cnndimreduc:
            if 'LSTM' == ag.rnn:
                # Safe to use one module many times in PyTorch
                hid0 = (self.dimreduc(hid0[0]), self.dimreduc(hid0[1]))
            else:
                hid0 = self.dimreduc(hid0)
        #print('inp', inp.shape, 'hid0', hid0)
        emb = self.drop(self.encoder(inp))
        #print('emb', emb.shape)
        out, hidn = self.rnn(emb, hid0)
        #print('out', out.shape, 'hidn', hidn.shape)
        dec = self.decoder(out)
        #print('dec', dec.shape)
        return dec, hidn

def evaluate():
    from statistics import mean

    class RotBar(object):
        def __init__(self):
            self.bars = '-\\|/' #self.bars = '←↖↑↗→↘↓↙'
            self.state = 0
        def get(self):
            bar = self.bars[self.state % len(self.bars)]
            self.state += 1
            return bar
    rotBar = RotBar()

    rnnmodel.eval()
    losses = []
    for iteration in range(int(len(dataloaderval))):
        imgB_, tokB_ = dataloaderval[iteration]

        tarB_ = np.pad(tokB_[:,1:], ((0, 0), (0, 1)), 'constant')
        tokB = th.autograd.Variable(th.from_numpy(tokB_.T), requires_grad=False)
        tarB = th.autograd.Variable(th.from_numpy(tarB_.T), requires_grad=False)
        tarB.contiguous()

        hid0 = th.from_numpy(imgB_[np.newaxis, :])
        hid0 = th.autograd.Variable(hid0, requires_grad=False)

        tokB = tokB.cuda() if ag.cuda else tokB
        hid0 = hid0.cuda() if ag.cuda else hid0
        tarB = tarB.cuda() if ag.cuda else tarB

        if 'LSTM' == ag.rnn:
            c0 = hid0.clone()#.zero_()
            c0 = c0.cuda() if ag.cuda else c0
            out, hid = rnnmodel(tokB, (hid0, c0))
        else:
            out, hid = rnnmodel(tokB, hid0)

        loss = crit(out.view(-1, vocab_len), tarB.view(-1))
        pred = out.view(-1, vocab_len).data.max(1)[1]
        correct = pred.eq(tarB.view(-1).data).cpu().sum()
        if False:
            capgen = Ltransn2w((out.cpu().data.max(2)[1]).numpy().T)
            #print('\033[31;1m<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\033[m')
            #pprint(Ltransn2w(tokB_))
            #print('\033[31;1m===================================\033[m')
            #pprint(capgen)
            #print('\033[31;1m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[m')
            pprint(random.choices(capgen, k=3))
        if False: print('\033[32;1m - TESTILNG iter', f'{iteration:>6d}', 'loss',
                f'{loss.data[0]:.2f}', '\taccuracy', correct, '/',
                out.view(-1, vocab_len).size(0), end='\033[m\n')
        losses.append(loss.data[0])
        print('\0337 - TESTING', rotBar.get(), iteration, len(dataloaderval), end='\0338')
        sys.stdout.flush()
    #print(losses)
    return mean(losses)

def train():
    curve = {}
    for iteration in range(ag.maxiter):
        rnnmodel.train()

        imgB_, tokB_ = dataloader.getBatch()
        #print(imgB_.shape, tokB_.shape)
        tarB_ = np.pad(tokB_[:,1:], ((0, 0), (0, 1)), 'constant')
        tokB = th.autograd.Variable(th.from_numpy(tokB_.T), requires_grad=False)
        tarB = th.autograd.Variable(th.from_numpy(tarB_.T), requires_grad=False)
        tarB.contiguous()

        hid0 = th.from_numpy(imgB_[np.newaxis, :])
        hid0 = th.autograd.Variable(hid0, requires_grad=False)

        tokB = tokB.cuda() if ag.cuda else tokB
        hid0 = hid0.cuda() if ag.cuda else hid0
        tarB = tarB.cuda() if ag.cuda else tarB

        if 'LSTM' == ag.rnn:
            c0 = hid0.clone()#.zero_()
            c0 = c0.cuda() if ag.cuda else c0
            out, hid = rnnmodel(tokB, (hid0, c0))
        else:
            out, hid = rnnmodel(tokB, hid0)

        loss = crit(out.view(-1, vocab_len), tarB.view(-1))
        optim.zero_grad()
        loss.backward()
        optim.step()
        pred = out.view(-1, vocab_len).data.max(1)[1]
        correct = pred.eq(tarB.view(-1).data).cpu().sum()
        if True:
            capgen = Ltransn2w((out.cpu().data.max(2)[1]).numpy().T)
            #print('\033[31;1m<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\033[m')
            #pprint(Ltransn2w(tokB_))
            #print('\033[31;1m===================================\033[m')
            #pprint(capgen)
            #print('\033[31;1m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[m')
            pprint(random.choices(capgen, k=3))
        print('\033[32;1m - iter', f'{iteration:>6d}', 'loss',
                f'{loss.data[0]:.2f}', '\taccuracy', correct, '/',
                out.view(-1, vocab_len).size(0), end='\033[m\n')
        curve[f'train/loss/{iteration}'] = loss.data[0]

        if (iteration+1)%ag.testevery == 0:
            testloss = evaluate()
            with open(f'{__file__}.rnnmodel.snapshot.{iteration}.pth', 'wb') as f:
                th.save(rnnmodel.state_dict(), f)
            curve[f'test/loss/{iteration}'] = testloss
    # post train
    with open(f'{__file__}.curve.{ag.maxiter}.pkl', 'wb') as f:
        pickle.dump(curve, f, pickle.HIGHEST_PROTOCOL)

def _makeCaption(cnnfeat, use_cuda, langmodel):
    langmodel.eval()

    hid0 = th.from_numpy(cnnfeat[np.newaxis, :]).unsqueeze(0)
    hid0 = th.autograd.Variable(hid0, requires_grad=False)
    hid0 = hid0.cuda() if ag.cuda else hid0

    x0 = th.autograd.Variable(th.ones((1, 1))).long()
    xn = x0.cuda() if use_cuda else x0
    hidn = hid0

    capout = []

    if 'LSTM' == ag.rnn:
        c0 = hid0.clone()
        c0 = c0.cuda() if ag.cuda else c0
        cn = c0
        for i in range(17):
            outn, (hidn, cn) = langmodel(xn, (hidn, cn))
            #print('outn, hidn, cn', outn.shape, hidn.shape, cn.shape)
            _, topi = outn.cpu().topk(1)
            topi = topi.view(-1)
            #print(topi, type(topi))
            capout.append(topi.data[0])
            #print(capout)
            xn = topi.view(-1).unsqueeze(0)
            xn = xn.cuda() if use_cuda else xn
            #print('xn shape', xn.shape)
    else:
        raise NotImplementedError #FIXME
        for i in range(17):
            outn, hidn = langmodel(xn, hidn)
    return [capout]
    #return (out.cpu().data.max(2)[1]).numpy().T

def makeCaption(imgpath, transform, extractor, use_cuda, langmodel):
    from extractfeature import imgRead
    img = imgRead(imgpath, transform, use_cuda)
    img = th.autograd.Variable(img.view(-1, 3, 224, 224))
    cnnfeat = extractor.forward(img)['fc'].data.numpy()
    capgeni = _makeCaption(cnnfeat, use_cuda, langmodel)
    capgen = Ltransn2w(capgeni)
    return capgen, capgeni

def CaptionGeneration(langmodel):
    import torchvision as vision
    from extractfeature import getExtractor, coco_transform_ten
    print('> [capgen] load validation dataset')
    with open(ag.cocoannoval, 'r') as f:
        json_val = json.load(f)
    print('> [capgen] load cnn and extractor')
    #cnn = vision.models.resnet18(pretrained=True)
    extractor = getExtractor(ag.cnn, ag.cuda)
    print('> [capgen] select random sample')
    sample = random.choice(json_val['images'])
    pprint(sample)
    call(['catimg', os.path.join(ag.cocopool, sample['file_name'])])
    print('\033[31;1m<<<<<<<<<<<<<<<[original sentences]<<<<<<<<<<<<<<<<<<<<\033[m')
    pprint([x['caption'] for x in json_val['annotations'] if x['image_id'] == sample['id']])
    print('\033[31;1m===================================\033[m')
    print(makeCaption(os.path.join(ag.cocopool, sample['file_name']),
        coco_transform_ten, extractor, ag.cuda, rnnmodel) )
    print('\033[31;1m>>>>>>>>>>>>>>>[ capgen sentences ]>>>>>>>>>>>>>>>>>>>>\033[m')

def extractSequenceFeature(rnnmodel):
    with open(ag.toks, 'rb') as f:
        toks = pickle.load(f)

    sentfeats = {}
    print('> extracting feature sequence')
    for n, (k, ltok) in enumerate(toks.items(), 1):
        ltok = [transw2i(tok) for tok in ltok]
        #print(ltok)
        maxlen = max(map(len, ltok)) + 2
        tokB = np.ndarray((len(ltok), maxlen), dtype=np.int)
        tokB.fill(0)
        for i, iv in enumerate(ltok):
            tokB[i, 0] = vocab_w2i['<start>']
            for j, jw in enumerate(iv):
                tokB[i, j+1] = jw
            tokB[i, len(iv)+1] = vocab_w2i['<end>']
        #print(tokB)

        tokB = th.autograd.Variable(th.from_numpy(tokB.T), requires_grad=False)
        hid0 = th.autograd.Variable(th.zeros(1,len(ltok),512), requires_grad=False)

        tokB = tokB.cuda() if ag.cuda else tokB
        hid0 = hid0.cuda() if ag.cuda else hid0

        if 'LSTM' == ag.rnn:
            c0 = hid0.clone()#.zero_()
            c0 = c0.cuda() if ag.cuda else c0
            out, (hid, c) = rnnmodel(tokB, (hid0, c0))
        else:
            out, hid = rnnmodel(tokB, hid0)

        #print(hid.shape)
        hid = hid.clone().cpu()
        hid = hid.data.numpy().squeeze()
        hid = [hid[i] for i in range(hid.shape[0])]
        #print(len(hid))
        sentfeats[k] = hid
        print('\0337 - ', n, '/', len(toks), end='\0338')
        sys.stdout.flush()
    print('> saving sentfeats')
    with open(f'{__file__}.sentfeats.pkl', 'wb') as f:
        pickle.dump(sentfeats, f)

def main_train():
    train()
    with open(f'{__file__}.rnnmodel.final.{ag.maxiter}.pth', 'wb') as f:
        th.save(rnnmodel.state_dict(), f)

def main_capgen():
    print('> Loading pre-trained rnn model')
    rnnmodel.load_state_dict(th.load(f'{__file__}.rnnmodel.final.{ag.maxiter}.pth'))
    CaptionGeneration(rnnmodel)

def main_hidn():
    print('> Loading pre-trained rnn model')
    rnnmodel.load_state_dict(th.load(f'{__file__}.rnnmodel.final.{ag.maxiter}.pth'))
    extractSequenceFeature(rnnmodel)

if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.set_defaults(func=ag.print_help)
    subag = ag.add_subparsers()
    # [train subparser]
    ag_train = subag.add_parser('train')
    ag_train.set_defaults(func=main_train)
    ag_train.add_argument('--featpool', type=str, default='./features')
    ag_train.add_argument('--cocoanno', type=str, default='../coco/annotations/captions_train2014.json')
    ag_train.add_argument('--cocoannoval', type=str, default='../coco/annotations/captions_val2014.json')
    ag_train.add_argument('--vocab', type=str, default='./buildvocab.py.vocab.pkl')
    ag_train.add_argument('--toks', type=str, default='./buildvocab.py.toks.pkl')
    ag_train.add_argument('--toksval', type=str, default='./buildvocab.py.toksval.pkl')
    ag_train.add_argument('--lr', type=float, default=1e-3)
    ag_train.add_argument('--batch', type=int, default=25)
    ag_train.add_argument('--optim', type=str, default='Adam')
    ag_train.add_argument('--maxiter', type=int, default=int(82783*7/25)) # 7 Epochs
    ag_train.add_argument('--testevery', type=int, default=int(82783*1.0/25)) # 0.5 Epoch
    ag_train.add_argument('--rnn', type=str, default='LSTM')
    ag_train.add_argument('--cuda', default=False, action='store_true')
    ag_train.add_argument('--cnndimreduc', default=False, action='store_true')
    ag_train.add_argument('--cnn', type=str, default='resnet18')
    # [capgen subparser]
    ag_capgen = subag.add_parser('capgen')
    ag_capgen.set_defaults(func=main_capgen)
    ag_capgen.add_argument('--cocopool', type=str, default='../coco/pool')
    # [hidn subparser] : dump hidden vector hidn
    ag_hidn = subag.add_parser('hidn')
    ag_hidn.set_defaults(func=main_hidn)
    # parse and dump
    ag = ag.parse_args()
    print('> Dump configuration')
    pprint(vars(ag))

    print('> Load Vocabulary')
    vocab_i2w, vocab_w2i, vocab_len = vocabmappings(ag.vocab)
    print('  - vocab length', vocab_len)

    print('> dataloader')
    dataloader = DataLoader()
    #dataloader.getBatch()
    dataloaderval = DataLoaderVal()

    print('> language model')
    rnnmodel = RNNmodel(vocab_len)
    rnnmodel = rnnmodel.cuda() if ag.cuda else rnnmodel
    print(rnnmodel)

    print('> loss function')
    crit = th.nn.CrossEntropyLoss()

    print('> optimizer')
    optim = getattr(th.optim, ag.optim)(rnnmodel.parameters(), lr=ag.lr, weight_decay=1e-7)

    ag.func()
