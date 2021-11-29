#!/usr/bin/python3
from pprint import pprint

# https://docs.python.org/3/library/index.html

# some Python3 built-in's

# https://docs.python.org/3/library/functions.html
# https://docs.python.org/3/library/constants.html
# https://docs.python.org/3/library/stdtypes.html
# https://docs.python.org/3/library/exceptions.html

# some Python3 STL's

from statistics import mean
print(mean([1,2,3,4]))

from statistics import median
print(median([1,2,3]))
print(median([1,2,3,4]))

from statistics import mode
print(mode([1,1,2,3,43,4,1,2]))
print(mode(['a', 'b', 'a', 'd']))

from statistics import variance, pvariance
print(variance([1,2,3]))
print(pvariance([1,2,3]))

import itertools
# TODO:

from functools import lru_cache, partial, partialmethod
from functools import singledispatch
# TODO:

import operator

import gzip

import configparser

import io

import urllib.request
import urllib.response
import urllib.parse

import turtle

import cmd

import shlex

import typing

import sys
import os

import contextlib

import gc
pprint(gc.get_stats())
