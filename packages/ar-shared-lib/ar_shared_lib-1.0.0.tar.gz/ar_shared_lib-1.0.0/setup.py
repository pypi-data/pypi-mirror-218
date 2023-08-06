#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
TEST_REQUIREMENTS = [i.strip() for i in open("tests/requirements.txt").readlines()]

setup(
    name='ar_shared_lib',
    version='1.0.0',
    description="A package that is shared across",
    author='Arthur Yatsun',
    author_email='arthur54342@gmail.com',
    url='',
    packages=find_packages(exclude=["tests*"]),
    python_requires='>=3.7',
    setup_requires=[
        "setuptools>=42",
        "wheel",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        "test": TEST_REQUIREMENTS,
    },
)
