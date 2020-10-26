# -*- coding: utf-8 -*-
from zope.testing import renormalizing

import doctest
import os
import sys
import unittest
import zc.buildout.testing


optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


def setUp(test):  # noqa
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('plone.recipe.codeanalysis', test)

    # Install any other recipes that should be available in the tests
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install('flake8', test)
    zc.buildout.testing.install('check-manifest', test)

    # Install second level install_requires dependencies
    zc.buildout.testing.install('pycodestyle', test)
    zc.buildout.testing.install('lxml', test)
    zc.buildout.testing.install('pyflakes', test)
    zc.buildout.testing.install('mccabe', test)
    zc.buildout.testing.install('zope.exceptions', test)
    zc.buildout.testing.install('zope.interface', test)


dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.endswith('.rst')]
tests.append('../README.rst')


# running buildouts in doctests breaks, only in py27, only on Travis
# well $*@! that.
if sys.version_info[0] < 3 and 'TRAVIS' in os.environ.keys():
    tests = []


def test_suite():
    suite = unittest.TestSuite((
        doctest.DocFileSuite(
            t,
            setUp=setUp,
            tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=optionflags,
            checker=renormalizing.RENormalizing([
                zc.buildout.testing.normalize_path,
            ]),
        )
        for t in tests
    ))
    return suite
