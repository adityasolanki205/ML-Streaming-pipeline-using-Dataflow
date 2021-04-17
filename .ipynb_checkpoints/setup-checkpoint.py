#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

setup(
    name='ml-deployment',
    version='0.1',
    author='Aditya',
    author_email = 'Aditya'
    install_requires=["numpy", 
                      "pandas", 
                      "google-cloud-storage", 
                      "scikit-learn", 
                      "joblib",
                      "google-cloud-pubsub", 
                      "googleapis-common-protos==1.5.3"
                     ],
    packages=find_packages(exclude=['data']),
    description='Dataflow sklearn Streaming',
    url=''
)