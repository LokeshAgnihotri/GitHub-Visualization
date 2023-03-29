#!/usr/bin/env python

from distutils.core import setup

import sys

if sys.version_info < (2, 7):
    sys.exit('Sorry, Python < 2.7 is not supported')


def readme():
    with open('readme.md') as f:
        return f.read()


setup(name='Splunk-HEC',
      python_requires='>2.7',
      version='1.81',
      description='This is a python class file for use with other python scripts to send events to a Splunk http event collector.',
      long_description=readme(),
      py_modules=['splunk_http_event_collector'],
      keywords="splunk hec",
      install_requires=[
          'requests'
      ],
      )
