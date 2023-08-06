"""
setup.py compile Cython code to C code.
"""
from distutils.extension import Extension

from setuptools import setup
from Cython.Build import cythonize
import numpy as np

extensions = [Extension("*", ["*.pyx"])]

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[np.get_include()]
)
