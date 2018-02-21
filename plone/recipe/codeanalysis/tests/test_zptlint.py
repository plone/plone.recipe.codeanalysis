# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from plone.recipe.codeanalysis.zptlint import console_script
from plone.recipe.codeanalysis.zptlint import ZPTLint
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os
import unittest


# TEST_ALL is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
ZPTLINT_INSTALLED = os.environ.get('TEST_ALL', False)
ZPTLINT_NOT_INSTALLED_MSG = 'zptlint is not installed'

VALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p tal:content="string:Hello World!" />
  </body>
</html>
"""

INVALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p tal:content="python:Hello World!" />
  </body>
</html>
"""


class TestZPTLint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestZPTLint, self).setUp()
        if os.path.isfile('../../bin/zptlint'):  # when cwd is parts/test
            self.options['zptlint-bin'] = '../../bin/zptlint'

    @unittest.skipIf(not ZPTLINT_INSTALLED, ZPTLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        with OutputCapture():
            self.assertFalse(ZPTLint(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['zptlint-bin'] = ''
        with OutputCapture():
            self.assertTrue(ZPTLint(self.options).run())

    @unittest.skipIf(not ZPTLINT_INSTALLED, ZPTLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        with OutputCapture():
            self.assertTrue(ZPTLint(self.options).run())

    @unittest.skipIf(not ZPTLINT_INSTALLED, ZPTLINT_NOT_INSTALLED_MSG)
    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            ZPTLint(self.options).run()
        file_exists = os.path.isfile(os.path.join(parts_dir, 'zptlint.log'))
        rmtree(parts_dir)
        self.assertTrue(file_exists)

    @unittest.skipIf(not ZPTLINT_INSTALLED, ZPTLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    @unittest.skipIf(not ZPTLINT_INSTALLED, ZPTLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
