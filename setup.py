#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


# Package meta-data.
NAME = 'django-notifs'
DESCRIPTION = 'Re-usable notification app for Django'
URL = 'https://github.com/danidee10/django-notifs'
EMAIL = 'osaetindaniel@gmail.com'
AUTHOR = 'Osaetin Daniel'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '2.6.2'

REQUIRED = ['django', 'pika', 'celery', 'six']
EXCLUDE = ['notifs', 'tests', '*.tests', '*.tests.*', 'tests.*']

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=EXCLUDE),
    install_requires=REQUIRED,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: All Rights Reserved',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
