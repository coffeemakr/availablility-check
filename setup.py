#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='avail',
      version='1.0',
      description='Availabilty Check',
      author_email='git@unstable.ch',
      install_requires=["requests"],
      py_modules=['avail'],
      entry_points={
          "console_scripts": [
              "avail = avail:run"
          ]
      }
    )