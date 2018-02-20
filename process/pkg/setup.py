# -*- encoding: utf-8 -*-
import re
import ast
from glob import glob
import os
from os.path import basename
from os.path import splitext

from setuptools import find_packages, setup

NAME = 'song_lyrics'
DESCRIPTION = 'Utility functions for the song lyrics project'
URL = ''
EMAIL = ''
AUTHOR = ''
LICENSE = 'GPL3'
LONG_DESCRIPTION = ''

REQUIRED = ['fuzzywuzzy', 'python-Levenshtein', 'pyyaml']

here = os.path.abspath(os.path.dirname(__file__))


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/song_lyrics/__init__.py', 'rb') as f:
    VERSION = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    url=URL,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path
                in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=REQUIRED,
    entry_points={},
)
