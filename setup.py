#!/usr/bin/env python

import os
from setuptools import setup

def package_files(directory):
    """Recursively add subfolders and files."""
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('notifications')

setup(name='django-notifs',
      version='1.7',
      description='Re-usable notification app for Django',
      url='https://github.com/danidee10/django-notifs',
      author='Osaetin Daniel',
      author_email='osaetindaniel@gmail.com',
      license='GPL',
      packages=['notifications'],
      package_data={'': extra_files},
      install_requires=[
          'django',
      ],
      zip_safe=False)
