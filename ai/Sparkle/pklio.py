'''
FlashLight: Personal PyTorch Helpers
Copyright (C) 2018 Mo Zhou
'''
from typing import *
import os
import _io
try:
    import dill as pickle
except:
    import pickle


def pklSave(obj: object, fpath: str) -> None:
    '''
    dump object to a file
    '''
    if isinstance(fpath, str):
        with open(fpath, 'wb') as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    elif isinstance(fpath, _io.BufferedWriter):
        pickle.dump(obj, fpath, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        raise TypeError(fpath)


def pklLoad(fpath: str) -> object:
    '''
    load object from file
    '''
    if isinstance(fpath, str):
        with open(fpath, 'rb') as f:
            return pickle.load(f)
    elif isinstance(fpath, _io.BufferedReader):
        return pickle.load(fpath)
    else:
        raise TypeError(fpath)




def test_pkl_saveload_path(tmpdir):
    fpath = str(tmpdir) + '/xxx.pkl'
    pklSave([fpath], fpath)
    assert(fpath == pklLoad(fpath)[0])
    os.remove(fpath)


def test_pkl_saveload_fd(tmpdir):
    fpath = str(tmpdir) + '/xxx.pkl'
    with open(fpath, 'wb') as f:
        pklSave([fpath], f)
    with open(fpath, 'rb') as f:
        assert(fpath == pklLoad(f)[0])
    os.remove(fpath)
