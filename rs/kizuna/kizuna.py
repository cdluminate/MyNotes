'''
kizuna is a dynamic computation graph engine, inspired by pytorch and tensorflow.
Copyright (C) 2018 Mo Zhou <cdluminate@gmail.com>, MIT License.
'''
from typing import *
from kinode import *


def node(*args):
    return kiNode(*args)


def ones(*args):
    return kiNode(np.ones(*args))


def rand(*args):
    return kiNode(np.random.random(*args))


def zeros(*args):
    return kiNode(np.zeros(*args))


def eye(*args):
    return kiNode(np.eye(*args))
