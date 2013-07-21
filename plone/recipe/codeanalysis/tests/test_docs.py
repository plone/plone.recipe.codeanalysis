# -*- coding: utf-8 -*-
"""
Doctest runner for 'plone.recipe.codeanalysis'.
"""
__docformat__ = 'restructuredtext'

import unittest
import doctest
import zc.buildout.tests
import zc.buildout.testing

from zope.testing import renormalizing

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

    # Seems like we have to install the dependencies defined in
    # install_requires manually to be available in the test
    # See:
    # http://mail.python.org/pipermail/distutils-sig/2009-December/014950.html
    zc.buildout.testing.install_develop('flake8', test)
    zc.buildout.testing.install_develop('zptlint', test)

def test_suite():
    suite = unittest.TestSuite((
        doctest.DocFileSuite(
            '../README.rst',
            setUp=setUp,
            tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=optionflags,
            checker=renormalizing.RENormalizing([
                # If want to clean up the doctest output you
                # can register additional regexp normalizers
                # here. The format is a two-tuple with the RE
                # as the first item and the replacement as the
                # second item, e.g.
                # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                zc.buildout.testing.normalize_path,
            ]),
        ),
    ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
