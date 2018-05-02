# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.importchecker import console_script
from plone.recipe.codeanalysis.importchecker import ImportChecker
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os
import unittest


# TEST_ALL is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
INSTALLED = os.environ.get('TEST_ALL', False)
NOT_INSTALLED_MSG = 'importchecker is not installed'

VALID_CODE = """\
import sys

def foo():
    print(sys.path)
"""

INVALID_CODE = """\
import sys

def foo():
    print('bar')
"""


class TestCleanLines(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestCleanLines, self).setUp()
        self.options.update({
            'importchecker': 'True',
        })
        if os.path.isfile('../../bin/importchecker'):  # when cwd is parts/test
            self.options['importchecker-bin'] = '../../bin/importchecker'

    @unittest.skipIf(not INSTALLED, NOT_INSTALLED_MSG)
    def test_analysis_should_return_false_if_unused_imports_are_found(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        with OutputCapture():
            self.assertFalse(ImportChecker(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['importchecker-bin'] = ''
        with OutputCapture():
            self.assertTrue(ImportChecker(self.options).run())

    @unittest.skipIf(not INSTALLED, NOT_INSTALLED_MSG)
    def test_analysis_should_return_true_for_valid_file(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        with OutputCapture():
            self.assertTrue(ImportChecker(self.options).run())

    @unittest.skipIf(not INSTALLED, NOT_INSTALLED_MSG)
    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        parts_dir = mkdtemp()
        self.given_a_file_in_test_dir('correct.py', VALID_CODE)
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            ImportChecker(self.options).run()
        file_exist = os.path.isfile(os.path.join(
            parts_dir, 'importchecker.log'))
        rmtree(parts_dir)
        self.assertTrue(file_exist)

    @unittest.skipIf(not INSTALLED, NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    @unittest.skipIf(not INSTALLED, NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
