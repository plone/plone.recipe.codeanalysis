# -*- coding: utf-8 -*-
"""
This module contains the tool of plone.recipe.codeanalysis
"""
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '2.1'

long_description = '\n\n'.join([
    read('README.rst'),
    read('plone', 'recipe', 'codeanalysis', 'README.rst'),
    read('CONTRIBUTORS.rst'),
    read('CHANGES.rst'),
])

entry_point = 'plone.recipe.codeanalysis:Recipe'
entry_points = {
    'zc.buildout': [
        'default = {0:s}'.format(entry_point)
    ]
}

setup(name='plone.recipe.codeanalysis',
      version=version,
      description='Static code analysis for buildout-based Python projects.',
      long_description=long_description,
      # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python',
          'Topic :: Software Development :: Build Tools',
      ],
      keywords='',
      author='Timo Stollenwerk',
      author_email='contact@timostollenwerk.net',
      url='http://github.com/plone/plone.recipe.codeanalysis/',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'check-manifest',
          'flake8>=2.0.0',
          'setuptools',
          'zc.buildout',
          'zc.recipe.egg',
      ],
      extras_require={
          'test': [
              'testfixtures',
              'zc.buildout [test]',
              'zope.testing',
          ],
          'recommended': [
              'flake8-blind-except',
              'flake8-coding',
              'flake8-debugger',
              'flake8-deprecated',
              'flake8-isort',
              'flake8-pep3101',
              'flake8-plone-api',
              'flake8-plone-hasattr',
              'flake8-print',
              'flake8-quotes',
              'flake8-string-format',
              'flake8-todo',
          ],
      },
      test_suite='plone.recipe.codeanalysis.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
