from setuptools import setup
from setuptools.config import read_configuration
from Cython.Build import cythonize

setup(ext_modules=cythonize('src/impkg/harmonic_mean.pyx'))

