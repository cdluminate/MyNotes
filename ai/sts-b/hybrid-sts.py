#!/usr/bin/env python3
'''
https://gluebenchmark.com/leaderboard
CBoW STS-B Pearson 61.2
BERT STS-B Pearson 87.6 (large) 87.1 (base)

Fine-tuned uncased_L-12_H-768_A-12 with regression loss (MSE):
STS-B Performance: r= 0.8858208062827871 p_value= 0.0

Test spaCy's pretrained model by the STS-B Task.
en_core_web_lg:
    weighted + doublenoun:
        r= 0.6227751034119451 p_value= 7.52452682670213e-162

Hybrid(Glove<1.0<BERT)    r=0.6265 min 0.0011 | max 1.0000 | mean 0.7606
Hybrid(Glove<0.9<BERT)    r=0.5860 min 0.0011 | max 0.9878 | mean 0.6704
Hybrid(Glove<0.8<BERT)    r=0.7912 min 0.0011 | max 0.9878 | mean 0.5596
Hybrid(Glove<0.7<BERT)    r=0.8738 min 0.0011 | max 0.9878 | mean 0.5252
Hybrid(Glove<0.6<BERT)    r=0.8852 min 0.0011 | max 0.9878 | mean 0.5202
Hybrid(Glove<0.5<BERT)    r=0.8860 min 0.0000 | max 0.9878 | mean 0.5198
Hybrid(Glove<0.4<BERT)    r=0.8858 min 0.0000 | max 0.9878 | mean 0.5201
Hybrid(Glove<0.3<BERT)    r=0.8858 min 0.0000 | max 0.9878 | mean 0.5201
Hybrid(Glove<0.2<BERT)    r=0.8858 min 0.0000 | max 0.9878 | mean 0.5201
Hybrid(Glove<0.1<BERT)    r=0.8858 min 0.0000 | max 0.9878 | mean 0.5201
Hybrid(Glove<0.0<BERT)    r=0.8858 min 0.0000 | max 0.9878 | mean 0.5201
'''
from typing import *
import os
import argparse
from collections import namedtuple

from tqdm import tqdm
import spacy
import scipy
import numpy as np
from scipy.stats import pearsonr
from scipy.spatial.distance import cosine
import pylab as lab
import zmq
import json

from stsData import *


def weightedSim(doc1, doc2, method='_my'):
    ''' doc1 and doc2 are both spacy document instances '''
    def _doublenouns2v(doc):
        vec = np.mean([(2*x.vector if x.pos_=='NOUN' else x.vector)
            for x in doc], axis=0)
        return vec if len(vec)>0 else doc.vector
    method = eval(f'{method}s2v')
    vec1, vec2 = method(doc1), method(doc2)
    return 1 - cosine(vec1, vec2)


class BertSTSLiveClient(object):
    '''
    Calculating STS using bert.
    Using the request-reply model.

    Pearson correlation on STS-B dataset: 0.88
    '''
    def __init__(self, addr='tcp://127.0.0.1:15555'):
        self.socket = zmq.Context().socket(zmq.REQ)
        self.socket.connect(addr)
    def __getitem__(self, query):
        '''
        Qeury format
        {'guid': 1, 'sent1': 'A man with a hard hat is dancing.',
                    'sent2': 'A man wearing a hard hat is dancing.' }
        '''
        if not isinstance(query, list) and len(query)!=3:
            raise ValueError
        request = json.dumps({
                'guid': query[0], 'sent1': query[1], 'sent2': query[2],
                })
        #print(request)
        self.socket.send_string(request)
        msg = self.socket.recv()
        score = json.loads(msg)['logits']
        #return score
        return np.clip(score/5., 0., 1.)  # \in [0, 1]
    def __call__(self, query):
        return self.__getitem__(query)

def stat(x: np.ndarray):
    return f'min {x.min():.4f} | max {x.max():.4f} | mean {x.mean():.4f}'

if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--datadir', type=str, required=True)
    ag.add_argument('--model', type=str, default='en_core_web_lg')
    ag.add_argument('--addr', type=str, default='tcp://172.16.1.2:15555')
    ag.add_argument('--sim', type=str, default='weighted')
    ag.add_argument('--method', type=str, default='_doublenoun')
    ag = ag.parse_args()

    # load data
    trainset, devset, testset = readDataset(ag)
    devgts = np.array([float(x.score) for x in devset])

    # evaluate bert
    bertcache = f'{__file__}.bert.npz'
    if not os.path.exists(bertcache):
        print('* Evaluating BERT ...')
        # start bert client
        bertclient = BertSTSLiveClient(addr=ag.addr)
        devscores_bert = np.zeros(len(devset))

        for i, rec in tqdm(enumerate(devset), total=len(devset)):
            req = (i, rec.sentence1, rec.sentence2)
            s = bertclient(req)  # isa float
            devscores_bert[i] = s
            #print(s, req)
        np.savez(bertcache, devscores_bert)
    else:
        print('* Loading cache for BERT ...')
        devscores_bert = np.load(bertcache)['arr_0']

    # report
    r, pval = pearsonr(devgts, devscores_bert)
    print(f'BERT | STS-B:', '\tr=', r, '\tp_value=', pval)

    # evaluate glove
    glovecache = f'{__file__}.glove.npz'
    if not os.path.exists(glovecache):
        print('* Evaluating GloVe ...')
        # load spacy model
        nlp = spacy.load(ag.model)
        devscores_glove = np.zeros(len(devset))

        for i, rec in tqdm(enumerate(devset), total=len(devset)):
            doc1 = nlp(rec.sentence1)
            doc2 = nlp(rec.sentence2)
            s = eval(f'{ag.sim}Sim')(doc1, doc2, method=ag.method)
            devscores_glove[i] = s
        np.savez(glovecache, devscores_glove)
    else:
        print('* Loading cache for GloVe ...')
        devscores_glove = np.load(glovecache)['arr_0']

    # report
    r, pval = pearsonr(devgts, devscores_glove)
    print(f'GloVe | STS-B:', '\tr=', r, '\tp_value=', pval)

    # hybrid model
    print()
    print('GT |', stat(devgts))
    print('BERT |', stat(devscores_bert))
    print('GloVe |', stat(devscores_glove))

    devscores_glove_nrm = (devscores_glove - 0.483)/(1.0-0.483)
    devscores_bert_nrm = (devscores_bert) #/ 5.0
    print('BERT nrm |', stat(devscores_bert_nrm))
    print('GloVe nrm |', stat(devscores_glove_nrm))

    print()
    for i in reversed(np.arange(11)/10):
        devscores = np.zeros(len(devset))
        for j in range(len(devset)):
            if devscores_glove[j] >= i:
                devscores[j] = devscores_bert_nrm[j]
            else:
                devscores[j] = devscores_glove_nrm[j]
        r, pval = pearsonr(devgts, devscores)
        print(f'Hybrid(Glove<{i}<BERT)', ' \t ', f'r={r:.4f}', stat(devscores))
