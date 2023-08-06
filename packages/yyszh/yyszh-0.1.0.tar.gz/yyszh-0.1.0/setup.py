#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='yyszh',
    version='0.1.0',
    description=(
        'utils for yyszhyyy'
    ),
    author='yyszh',
    author_email='navinfo_nlp@163.com',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'xlrd==1.2.0',
        'numpy',
        'tqdm',
        'python-docx',
        'configparser',
        'xlsxwriter==3.0.1'
    ],
)
