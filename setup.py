#!/usr/bin/env python

from distutils.core import setup

setup(name='avail',
      version='1.0',
      description='Availabilty Check',
      author_email='git@unstable.ch',
      install_requires=["requests"],
      py_modules=['avail'],
     )