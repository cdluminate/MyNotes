#!/usr/bin/python3
from distutils.core import setup, Extension

'''
https://docs.python.org/3/extending/building.html#building

build this package with this command
$ python3 setup.py build
$ python3 setup.py install
'''

module = Extension('my',
  sources = ['mymodule.c'])

setup (name = 'my',
  version = '0a',
  description = 'this is a test package',
  ext_modules = [module])

