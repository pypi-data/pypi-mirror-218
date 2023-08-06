#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
import re

# result = re.search(r'(\d+)\.(\d+)\.(\d+)', open('version.in').read())
# major = result.group(1)
# minor = result.group(2)
# patch = int(result.group(3)) + 1
# version = f'{major}.{minor}.{patch}'
# open('version.in','w').write(version)

setup(
    platforms=['win-amd64'],
    name='practistyle',
    version='0.0.76',
    author='sl.truman',
    author_email='sl.truman@live.com',
    url='',
    description=u'',
    packages=['practistyle','practistyle/end_effector','py3dbp','practistyle/data'],
    # install_requires=[
    #     'numpy',
    #     'pybullet',
    #     'scipy'
    # ],
    include_package_data=True
) 
