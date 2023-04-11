'''
Test spaCy's pretrained model by the STS-B Task.

en_core_web_sm:
    plain:
        r= 0.4123684260842511 p_value= 1.1700745997228377e-62
    weighted + doublenoun:
        r= 0.4222328421415563 p_value= 6.533978440565753e-66
    weighted + nostopdoublenoun:
        r= 0.41174397504580384 p_value= 1.8642337792099999e-62
    weighted + nostop:
        r= 0.4039982423937323 p_value= 5.549126250568965e-60

en_core_web_lg:
    plain:
        r= 0.5437706331109512 p_value= 3.587169985056182e-116
    weighted + nostop:
        r= 0.5437706275727905 p_value= 3.587192997746199e-116
    weighted + nostopdoublenoun:
        r= 0.6227751034119451 p_value= 7.52452682670213e-162
    weighted + doublenoun:
        r= 0.6227751034119451 p_value= 7.52452682670213e-162
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

from stsData import *


def plainSim(doc1, doc2, method=None):
    ''' doc1 and doc2 are both spacy document instances '''
    return doc1.similarity(doc2)


def weightedSim(doc1, doc2, method='_my'):
    ''' doc1 and doc2 are both spacy document instances '''
    def _nostops2v(doc):
        vec = np.mean([x.vector for x in doc if not x.is_stop], axis=0)
        return vec if len(vec)>0 else doc.vector
    def _nostopdoublenouns2v(doc):
        vec = np.mean([(2*x.vector if x.pos_=='NOUN' else x.vector)
            for x in doc if not x.is_stop], axis=0)
        return vec if len(vec)>0 else doc.vector
    def _doublenouns2v(doc):
        vec = np.mean([(2*x.vector if x.pos_=='NOUN' else x.vector)
            for x in doc], axis=0)
        return vec if len(vec)>0 else doc.vector
    method = eval(f'{method}s2v')
    vec1, vec2 = method(doc1), method(doc2)
    return 1 - cosine(vec1, vec2)


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--datadir', type=str, required=True)
    ag.add_argument('--model', type=str, default='en_core_web_sm')
    ag.add_argument('--sim', type=str, default='plain')
    ag.add_argument('--method', type=str, default='_doublenoun')
    ag.add_argument('--saveto', type=str, default=f'{__file__}.predict')
    ag = ag.parse_args()

    trainset, devset, testset = readDataset(ag)

    nlp = spacy.load(ag.model)

    devgts = np.array([float(x.score) for x in devset])
    devscores = np.zeros(len(devset))

    for i, rec in tqdm(enumerate(devset), total=len(devset)):
        doc1 = nlp(rec.sentence1)
        doc2 = nlp(rec.sentence2)
        s = eval(f'{ag.sim}Sim')(doc1, doc2, method=ag.method)
        devscores[i] = s

    r, pval = pearsonr(devgts, devscores)
    print(f'STS-B Performance:', '\tr=', r, '\tp_value=', pval)
    np.savetxt(ag.saveto, devscores)
