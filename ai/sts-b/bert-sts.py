#!/usr/bin/python3
'''
Fine-tuned uncased_L-12_H-768_A-12 with regression loss (MSE):
STS-B Performance: 	r= 0.8858208062827871 	p_value= 0.0
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


def draw():
    import numpy as np
    import pylab as lab

    y, x = np.load('./bert-sts.py.gt-bert.npz')['arr_0']
    lab.scatter(x, y)
    lab.xlabel('Predicted Similarity')
    lab.ylabel('Human Score')
    lab.grid()
    lab.savefig('bert-sts.svg')


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--datadir', type=str, required=True)
    ag.add_argument('--addr', type=str, default='tcp://172.16.1.2:15555')
    ag = ag.parse_args()

    bertclient = BertSTSLiveClient(addr=ag.addr)
    trainset, devset, testset = readDataset(ag)

    devgts = np.array([float(x.score) for x in devset])
    devscores = np.zeros(len(devset))

    for i, rec in tqdm(enumerate(devset), total=len(devset)):
        req = (i, rec.sentence1, rec.sentence2)
        s = bertclient(req)  # isa float
        devscores[i] = s
        #print(s, req)

    r, pval = pearsonr(devgts, devscores)
    print(f'STS-B Performance:', '\tr=', r, '\tp_value=', pval)

    print('Saving evaluation results')
    np.savez(f'{__file__}.gt-bert.npz', (devgts, devscores))
