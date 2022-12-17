'''
Test spaCy's pretrained model by the STS-B Task using Co-occurrence.

en_core_web_sm:
    IoU / plain:
        r= 0.6531936541502584
    IoU / nostop:
        r= 0.6806135828588004
    IoU / donoun:
        r= 0.6746403116157866
    IoU / nostopdonoun:
        r= 0.7035425066766811

Raw COOC value doesn't work.
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

from stsData import *


def iouSim(doc1, doc2, method):
    def _plain(doc1, doc2) -> float:
        lemma1 = set(x.lemma_ for x in doc1)
        lemma2 = set(x.lemma_ for x in doc2)
        inter = set.intersection(lemma1, lemma2)
        union = set.union(lemma1, lemma2)
        if len(union) == 0: return 0.
        return len(inter)/len(union)
    def _nostop(doc1, doc2) -> float:
        lemma1 = set(x.lemma_ for x in doc1 if not x.is_stop)
        lemma2 = set(x.lemma_ for x in doc2 if not x.is_stop)
        inter = set.intersection(lemma1, lemma2)
        union = set.union(lemma1, lemma2)
        if len(union) == 0: return 0.
        return len(inter)/len(union)
    def _donoun(doc1, doc2) -> float:
        lemma1 = set(x.lemma_ for x in doc1)
        lemma2 = set(x.lemma_ for x in doc2)
        inter = set.intersection(lemma1, lemma2)
        union = set.union(lemma1, lemma2)
        bonus = sum([(x.lemma_ in inter) for x in doc1 if 'NOUN'==x.pos_])
        if len(union) == 0: return 0.
        return (bonus + len(inter))/(bonus + len(union))
    def _nostopdonoun(doc1, doc2) -> float:
        lemma1 = set(x.lemma_ for x in doc1 if not x.is_stop)
        lemma2 = set(x.lemma_ for x in doc2 if not x.is_stop)
        inter = set.intersection(lemma1, lemma2)
        union = set.union(lemma1, lemma2)
        bonus = sum([(x.lemma_ in inter) for x in doc1 if 'NOUN'==x.pos_])
        if len(union) == 0: return 0.
        return (bonus + len(inter))/(bonus + len(union))
    return eval(f'{method}')(doc1, doc2)


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--datadir', type=str, required=True)
    ag.add_argument('--model', type=str, default='en_core_web_sm')
    ag.add_argument('--sim', type=str, default='plain')
    ag.add_argument('--method', type=str, default='_doublenoun')
    ag.add_argument('--saveto', type=str, default=f'{__file__}')
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
    np.savetxt(ag.saveto + '.predict', devscores)

    lab.scatter(devscores, devgts)
    lab.xlabel('Prediction')
    lab.ylabel('Human Score')
    lab.savefig(ag.saveto + '.svg')
