# -*- coding: utf-8 -*-
"""
This module contains the tool of plone.recipe.codeanalysis
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0b2'

long_description = (
    read('README.rst')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('plone', 'recipe', 'codeanalysis', 'README.rst')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.rst')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.rst')
    + '\n' +
    'Download\n'
    '********\n')

entry_point = 'plone.recipe.codeanalysis:Recipe'
entry_points = {
  "zc.buildout": [
    "default = %s" % entry_point
  ]
}

tests_require = [
  'zope.testing', 'zc.buildout[test]',
]

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
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
        'flake8',
        'zptlint',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='plone.recipe.codeanalysis.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
