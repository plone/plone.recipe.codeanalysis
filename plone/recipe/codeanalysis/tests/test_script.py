# -*- coding: utf-8 -*-
from contextlib import contextmanager
from plone.recipe.codeanalysis import code_analysis
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os
import sys
import unittest


INVALID_CODE = """
from plone.recipe.codeanalysis import code_analysis
"""

VALID_CODE = """
# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis import code_analysis

code_analysis()
"""


@contextmanager
def wrap_sys_argv():
    """Super simple context manager to clean sys.argv"""
    # setup
    old_sys = sys.argv
    sys.argv = []

    # give control back
    yield

    # restore
    sys.argv = old_sys


class TestScripts(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.realpath(mkdtemp())
        for directory in ('bin', 'parts', 'eggs', 'develop-eggs'):
            os.makedirs('{0}/{1}'.format(test_dir, directory))

        self.test_dir = test_dir
        self.options = {
            'flake8-extensions': 'flake8-coding',
            'flake8': 'True',
            'return-status-codes': 'False',
            'directory': self.test_dir,
            'multiprocessing': 'False',
        }
        if os.path.isfile('../../bin/flake8'):  # when cwd is parts/test
            self.options['bin-directory'] = '../../bin'

        valid_file = '{0}/parts/valid.py'.format(self.test_dir)
        invalid_file = '{0}/eggs/invalid.py'.format(self.test_dir)

        with open(valid_file, 'w') as valid_file:
            valid_file.write(VALID_CODE)

        with open(invalid_file, 'w') as invalid_file:
            invalid_file.write(INVALID_CODE)

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_default_directory(self):
        with OutputCapture() as output:
            with wrap_sys_argv():
                sys.argv = [
                    'bin/code-analysis',
                ]
                code_analysis(self.options)

        self.assertIn(
            'C101 Coding magic comment not found',
            output.captured,
        )

    def test_another_directory(self):
        # the invalid file is on eggs
        folder = '{0}/parts'.format(self.test_dir)
        with OutputCapture() as output:
            with wrap_sys_argv():
                sys.argv = [
                    'bin/code-analysis',
                    folder,
                ]
                code_analysis(self.options)

        self.assertNotIn(
            'C101 Coding magic comment not found',
            output.captured,
        )
