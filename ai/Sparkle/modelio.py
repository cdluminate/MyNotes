from typing import *
import os
import torch as th
import pytest


def modelSave(model: Any, dest: str, *, score=0., note='', verb=True):
    '''
    Serialize the model into a binary file, together with
    the score of the model and possibly some notes.
    '''
    if verb: print(f'=> Saving model to {dest}, score {score}')
    if verb: print(f' . {note}')
    try:
        _ = getattr(model, 'state_dict')
        pack = [model.state_dict(), score, note]
    except AttributeError:
        pack = [model, score, note]
    th.save(pack, dest)


def modelLoad(src: str, *, verb=True):
    state, score, note = th.load(src)
    if verb: print(f'=> Loading model from {src}, score {score}')
    if verb and isinstance(note, str): print(f' . {note}')
    elif verb and isinstance(note, list):
        for n in note: print(f' . {n}')
    return state, score, note


def test_saveload_state(tmpdir):
    dest = str(tmpdir) + f'/{os.path.basename(__file__)}.pt'
    l = th.nn.Linear(10, 10)
    modelSave(l, dest, score=1., note='test', verb=False)
    state, score, note = modelLoad(dest, verb=False)
    assert(score == 1.)
    assert(note == 'test')

def test_saveload_other(tmpdir):
    dest = str(tmpdir) + f'/{os.path.basename(__file__)}.pt'
    x = ['abcabc', 123, {123, 456}]
    modelSave(x, dest, verb=False)
    state, _, _ = modelLoad(dest, verb=False)
    assert(state[0] == 'abcabc')
    assert(state[1] == 123)
    assert(state[2] == {123, 456})

def test_saveload_note(tmpdir):
    dest = str(tmpdir) + f'/{os.path.basename(__file__)}.pt'
    modelSave([], dest, note=['note1', 'note2'], verb=False)
    _, _, note = modelLoad(dest, verb=False)
    assert(note[0] == 'note1')
    assert(note[1] == 'note2')
