'''
Test Elmo pretrained model by the STS-B Task.
https://github.com/allenai/allennlp/blob/master/tutorials/how_to/elmo.md

slice 0 (1024)
STS-B Performance: 	r= 0.6732629558221748 	p_value= 1.1742080772574129e-198
slice 1 (1024)
STS-B Performance: 	r= 0.6318097338109869 	p_value= 6.176117922255675e-168
slice 2 (1024)
STS-B Performance: 	r= 0.6550661090574728 	p_value= 1.4265953221021864e-184
concatenation of three slices (3072)
STS-B Performance: 	r= 0.662239430517443 	p_value= 5.251949057429555e-190
'''
from typing import *
import os
import argparse
from collections import namedtuple

from tqdm import tqdm
import scipy
import numpy as np
from scipy.stats import pearsonr
from allennlp.commands.elmo import ElmoEmbedder
import spacy
import torch as th

from stsData import *


if __name__ == '__main__':

    ag = argparse.ArgumentParser()
    ag.add_argument('--datadir', type=str, required=True)
    ag.add_argument('--config', type=str,
        default=os.path.expanduser('~/elmo/elmo_2x4096_512_2048cnn_2xhighway_options.json'))
    ag.add_argument('--weights', type=str,
        default=os.path.expanduser('~/elmo/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5'))
    ag.add_argument('--model', type=str, default='en_core_web_sm')
    ag.add_argument('-D', '--device', type=int, default=-1)
    ag = ag.parse_args()

    trainset, devset, testset = readDataset(ag)

    elmo = ElmoEmbedder(ag.config, ag.weights, ag.device)
    nlp = spacy.load('en_core_web_sm')

    devgts = np.array([float(x.score) for x in devset])
    devscores = np.zeros(len(devset))

    for i, rec in tqdm(enumerate(devset), total=len(devset)):
        # tokenization
        tokens1 = [x.text for x in nlp(rec.sentence1)]
        tokens2 = [x.text for x in nlp(rec.sentence2)]

        # embedding
        with th.no_grad():
            vec1 = elmo.embed_sentence(tokens1).mean(1).reshape(-1)
            vec2 = elmo.embed_sentence(tokens2).mean(1).reshape(-1)

            # similarity
            s = 1 - scipy.spatial.distance.cosine(vec1, vec2)
            devscores[i] = s

    r, pval = pearsonr(devgts, devscores)
    print(f'STS-B Performance:', '\tr=', r, '\tp_value=', pval)
