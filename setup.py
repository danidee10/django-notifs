#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


# Package meta-data.
NAME = 'django-notifs'
DESCRIPTION = 'Modular notifications for Django'
URL = 'https://github.com/danidee10/django-notifs'
EMAIL = 'osaetindaniel@gmail.com'
AUTHOR = 'Osaetin Daniel'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '2.6.4'

REQUIRED = ['django>=2.0', 'pika', 'celery<=4.1.0']
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
    license='MIT'
)
