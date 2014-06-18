# -*- coding: utf-8 -*-
"""
This module contains the tool of plone.recipe.codeanalysis
"""
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0rc1'

long_description = (
    read('README.rst')
    + '\n\n' +
    read('plone', 'recipe', 'codeanalysis', 'README.rst')
    + '\n\n' +
    read('CONTRIBUTORS.rst')
    + '\n\n' +
    read('CHANGES.rst')
    + '\n\n' +
    'Download\n'
    '********\n')

entry_point = 'plone.recipe.codeanalysis:Recipe'
entry_points = {
    "zc.buildout": [
        "default = %s" % entry_point
    ]
}

setup(name='plone.recipe.codeanalysis',
      version=version,
      description="Static code analysis for buildout-based Python projects.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
      ],
      keywords='',
      author='Timo Stollenwerk',
      author_email='contact@timostollenwerk.net',
      url='http://github.com/plone/plone.recipe.codeanalysis/',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'flake8',
          'setuptools',
          'zc.buildout',
          'zc.recipe.egg',
      ],
      extras_require={
          'test': [
              'mock',
              'zc.buildout [test]',
              'zope.testing',
          ],
      },
      test_suite='plone.recipe.codeanalysis.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
