#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import find_packages, setup


# Package meta-data.
NAME = 'django-notifs'
DESCRIPTION = 'Modular notifications for Django'
URL = 'https://github.com/danidee10/django-notifs'
EMAIL = 'osaetindaniel@gmail.com'
AUTHOR = 'Osaetin Daniel'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '3.0.2'

REQUIRED = [
    'django>=2.0', 'requests==2.25.1', 'django-jsonfield-backport==1.0.3'
]
TEST_REQUIRES = ['coverage>=5.4']
EXTRAS_REQUIRE = {
    'celery': ['celery>=4.1.0'],
    'rq': ['django-rq>=2.4.0'],
    'channels': ['channels>=3.0.3', 'channels-redis>=3.2.0']
}
EXCLUDE = ['notifs', 'tests', '*.tests', '*.tests.*', 'tests.*']

current_directory = path.abspath(path.dirname(__file__))
with open(path.join(current_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=EXCLUDE),
    install_requires=REQUIRED,
    test_requires=TEST_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    license='MIT'
)
