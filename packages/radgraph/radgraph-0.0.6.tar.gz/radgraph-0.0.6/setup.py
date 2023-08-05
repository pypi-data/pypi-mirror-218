import pathlib
import sys
from setuptools import setup, find_packages

setup(
    name='radgraph',
    version='0.0.6',
    author='Jean-Benoit Delbrouck',
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=['torch>=1.8.1',
                      'transformers>=4.23.1',
                      "appdirs",
                      'overrides==3.1.0',
                      'jsonpickle',
                      'filelock',
                      'h5py',
                      'spacy',
                      'nltk',
                      ],
    packages=find_packages(),
    zip_safe=False)
