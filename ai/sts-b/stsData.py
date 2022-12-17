from typing import *
import types
import os
import argparse
from collections import namedtuple


def readDataset(ag):
    '''
    Load the STS-B dataset from the given directory.
    It requires the original data.
    '''
    if not os.path.exists(ag.datadir):
        raise FileNotFoundError(ag.datadir)

    Record = namedtuple('Record', 'genre filename year old_index score sentence1 sentence2')

    def _readDataset(fpath: str):
        lines = open(fpath, 'r').readlines()
        lines = [line.strip().split('\t') for line in lines]
        lines = [Record(*line[:7]) for line in lines]
        return lines

    # sts-train.tsv
    train = _readDataset(os.path.join(ag.datadir, 'sts-train.tsv'))
    # sts-dev.tsv
    val   = _readDataset(os.path.join(ag.datadir, 'sts-dev.tsv'))
    # sts-test.tsv
    test  = _readDataset(os.path.join(ag.datadir, 'sts-test.tsv'))

    #print(f' * STS-B Dataset Size: train {len(train)}, val {len(val)}, test {len(test)}')
    return train, val, test


if __name__ == '__main__':

    ag = types.SimpleNamespace(datadir=os.path.expanduser('~/GLUE/STS-B/original'))
    train, val, test = readDataset(ag)
    print(f'train {len(train)}, val {len(val)}, test {len(test)}')
