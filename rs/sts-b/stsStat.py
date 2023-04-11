import importlib
import os
import sys
import argparse
import pylab as lab
import numpy as np
from scipy.stats import pearsonr

from stsData import *


def _requires_(ag, l):
    '''
    Checks whether an object has all the desired attributes.
    '''
    for x in l:
        if not hasattr(ag, x):
            raise AttributeError(f'Missing {x} argument')
    return True


def main_hist(ag):
    '''
    Histogram of human scores.
    '''
    _requires_(ag, ['datadir', 'saveto'])
    train, val, test = readDataset(ag)
    scores = np.array([x.score for x in train], dtype=float)
    valscores = np.array([x.score for x in val], dtype=float)
    print('* mean, std, min, max')
    print(scores.mean(), scores.std(), scores.min(), scores.max())
    lab.hist(scores)
    lab.savefig(ag.saveto)
    np.savetxt(f'{__file__}.dev.ground_truth', valscores)


def main_histogram(ag):
    '''
    Histogram of any list of scores
    '''
    _requires_(ag, ['predict', 'saveto'])
    scores = np.loadtxt(ag.predict)
    print(scores.shape)
    hist = np.histogram(scores, bins=50)
    print(hist[0].shape, hist[0])
    print(hist[1])
    lab.hist(scores, bins=50, density=True)
    lab.plot(np.arange(len(hist[0]))*5/(len(hist[0])), np.cumsum(hist[0])/np.sum(hist[0]))
    lab.grid(True)
    lab.show()
    cumsum = np.cumsum(hist[0]/sum(hist[0]))
    print('Cumsum', cumsum)
    for i, j in zip(cumsum, hist[1]):
        print('Cumsum/Score', i, '\t', j)
    #lab.savefig(ag.saveto)


def main_scatterhp(ag):
    '''
    make scatter plot: x=prediction, y=human(STS-B/dev)
    '''
    _requires_(ag, ['datadir', 'predict'])
    train, val, test = readDataset(ag)
    scores = np.array([x.score for x in val], dtype=float)
    predict = np.loadtxt(ag.predict).reshape(-1)
    print('PearsonR', pearsonr(scores, predict))
    lab.scatter(predict, scores)
    lab.xlabel('Prediction')
    lab.ylabel('Human Score')
    lab.show()


def main_scatter(ag):
    '''
    make scatter plot: generic: x=predict, y=golden
    '''
    _requires_(ag, ['predict', 'golden'])
    predict = np.loadtxt(ag.predict)
    golden = np.loadtxt(ag.golden)
    print('PearsonR', pearsonr(predict, golden))
    lab.scatter(predict, golden)
    lab.xlabel(os.path.basename(ag.predict))
    lab.ylabel(os.path.basename(ag.golden))
    lab.show()



if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('-S', '--sub', type=str, required=True)
    ag.add_argument('--saveto', type=str, default=f'{__file__}.svg')
    ag.add_argument('--datadir', type=str, default=None)
    ag.add_argument('--predict', type=str, default=None)
    ag.add_argument('--golden', type=str, default=None)
    ag = ag.parse_args()

    eval(f'main_{ag.sub}')(ag)
