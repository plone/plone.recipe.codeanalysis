# -*- coding: utf-8 -*-
"""
Doctest runner for 'plone.recipe.codeanalysis'.
"""
__docformat__ = 'restructuredtext'

from zope.testing import renormalizing

import doctest
import os
import unittest
import zc.buildout.testing
import zc.buildout.tests

optionflags = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_ONLY_FIRST_FAILURE
)


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('plone.recipe.codeanalysis', test)

    # Install any other recipes that should be available in the tests
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install('flake8', test)
    zc.buildout.testing.install('zptlint', test)
    zc.buildout.testing.install('i18ndude', test)

    # Install second level install_requires dependencies
    zc.buildout.testing.install('pep8', test)
    zc.buildout.testing.install('pyflakes', test)
    zc.buildout.testing.install('pytz', test)
    zc.buildout.testing.install('mccabe', test)
    zc.buildout.testing.install('six', test)
    zc.buildout.testing.install('ordereddict', test)
    zc.buildout.testing.install('plone.i18n', test)
    zc.buildout.testing.install('unidecode', test)
    #zc.buildout.testing.install('transaction', test)
    zc.buildout.testing.install('zope.browser', test)
    zc.buildout.testing.install('zope.component', test)
    zc.buildout.testing.install('zope.configuration', test)
    zc.buildout.testing.install('zope.contentprovider', test)
    zc.buildout.testing.install('zope.contenttype', test)
    zc.buildout.testing.install('zope.event', test)
    zc.buildout.testing.install('zope.exceptions', test)
    zc.buildout.testing.install('zope.i18n', test)
    zc.buildout.testing.install('zope.i18nmessageid', test)
    zc.buildout.testing.install('zope.interface', test)
    zc.buildout.testing.install('zope.location', test)
    zc.buildout.testing.install('zope.pagetemplate', test)
    zc.buildout.testing.install('zope.publisher', test)
    zc.buildout.testing.install('zope.proxy', test)
    zc.buildout.testing.install('zope.schema', test)
    zc.buildout.testing.install('zope.security', test)
    zc.buildout.testing.install('zope.tal', test)
    zc.buildout.testing.install('zope.tales', test)
    zc.buildout.testing.install('zope.traversing', test)


dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.endswith('.rst')]
tests.append('../README.rst')


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
