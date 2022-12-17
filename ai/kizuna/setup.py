from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np

ext_modules = cythonize([
        Extension('kinode', ['kinode.pyx']),
        ])

setup(
        name='kizuna',
        ext_modules=ext_modules
)
