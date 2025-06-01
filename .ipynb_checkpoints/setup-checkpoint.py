#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

setup(
    name='ml-deployment',
    version='0.1',
    author='Aditya',
    author_email = 'Aditya',
    install_requires=["apache-beam[gcp]==2.64.0",
                      "numpy", 
                      "pandas", 
                      "google-cloud-storage", 
                      "scikit-learn", 
                      "joblib==1.1.0",
                      "google-cloud-pubsub", 
                      "googleapis-common-protos==1.5.10"
                     ],
    packages=find_packages(exclude=['data']),
    description='Dataflow sklearn Streaming',
    url=''
)