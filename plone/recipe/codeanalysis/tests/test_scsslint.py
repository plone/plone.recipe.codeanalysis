# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from plone.recipe.codeanalysis.scsslint import console_script
from plone.recipe.codeanalysis.scsslint import SCSSLint
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os
import unittest


# TEST_ALL is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
SCSSLINT_INSTALLED = os.environ.get('TEST_ALL', False)
SCSSLINT_NOT_INSTALLED_MSG = 'scsslint is not installed'

CORRECT_SCSS = """\
.foo {
  font-size: larger;
}
"""

INCORRECT_SCSS = """\
.foo {
    font-size: larger;
}
"""

NOINDENTATION_CONFIG = """\
linters:
  Indentation:
    enabled: false
"""


class TestSCSSLint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestSCSSLint, self).setUp()
        if os.path.isfile('../../bin/scss-lint'):  # when cwd is parts/test
            self.options['scsslint-bin'] = '../../bin/scss-lint'

        self.given_a_file_in_test_dir('correct.scss', CORRECT_SCSS)

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('incorrect.scss', INCORRECT_SCSS)
        with OutputCapture():
            self.assertFalse(SCSSLint(self.options).run())

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true_when_config_ignores_error(self):
        config = self.given_a_file_in_test_dir('scss.config',
                                               NOINDENTATION_CONFIG)
        self.options['scsslint-config'] = config
        self.given_a_file_in_test_dir('incorrect.scss', INCORRECT_SCSS)
        with OutputCapture():
            self.assertTrue(SCSSLint(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['csslint-bin'] = 'FAKE_BIN'
        with OutputCapture():
            self.assertTrue(SCSSLint(self.options).run())

    def test_analysis_should_return_true(self):
        with OutputCapture():
            self.assertTrue(SCSSLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            SCSSLint(self.options).run()
        file_exist = os.path.isfile(os.path.join(parts_dir, 'scsslint.xml'))
        self.assertTrue(file_exist)
        rmtree(parts_dir)

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_file_contains_xml_warnings_when_jenkins_is_true(self):
        self.given_a_file_in_test_dir('incorrect.scss', INCORRECT_SCSS)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            SCSSLint(self.options).run()
        with open(os.path.join(parts_dir, 'scsslint.xml')) as fh:
            warnings = fh.read()
        self.assertTrue(warnings.startswith('<?xml'))
        self.assertIn('<error', warnings)
        self.assertIn('line="2"', warnings)
        self.assertIn('severity="warning"', warnings)
        self.assertIn('Line should be indented 2 spaces', warnings)
        rmtree(parts_dir)

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('incorrect.scss', INCORRECT_SCSS)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
