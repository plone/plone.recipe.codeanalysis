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

RUBY_DEPRECATED_XML = """\
DEPRECATION WARNING:
Sass 3.5 will no longer support Ruby 1.9.3.
Please upgrade to Ruby 2.0.0 or greater as soon as possible.

<?xml version="1.0" encoding="utf-8"?>
<checkstyle version="1.5.6">
  <file name="/srv/jenkins-slave/var/jenkins/workspace/branch-OPS-798-jenkins-code-analysis-shouldfail-md.widget/src/md/widget/OPS-798-fail/fail.scss">
    <error source="" line="2" column="1" length="1" severity="error" message="Syntax Error: Invalid CSS after &quot;#boom#&quot;: expected &quot;{&quot;, was &quot;&quot;" />
  </file>
</checkstyle>
"""  # flake8:noqa

class TestSCSSLint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestSCSSLint, self).setUp()
        if os.path.isfile('../../bin/scss-lint'):  # when cwd is parts/test
            self.options['scsslint-bin'] = '../../bin/scss-lint'

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('incorrect.scss', INCORRECT_SCSS)
        with OutputCapture():
            self.assertFalse(SCSSLint(self.options).run())

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true_when_config_ignores_error(self):
        self.given_a_file_in_test_dir('correct.scss', CORRECT_SCSS)
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

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('correct.scss', CORRECT_SCSS)
        with OutputCapture():
            self.assertTrue(SCSSLint(self.options).run())

    def test_analysis_should_return_true_without_scss(self):
        with OutputCapture():
            self.assertTrue(SCSSLint(self.options).run())

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        self.given_a_file_in_test_dir('correct.scss', CORRECT_SCSS)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            returnvalue = SCSSLint(self.options).run()
        file_exist = os.path.isfile(os.path.join(parts_dir, 'scsslint.xml'))
        rmtree(parts_dir)
        self.assertTrue(file_exist)
        self.assertTrue(returnvalue)

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_file_contains_xml_when_jenkins(self):
        self.given_a_file_in_test_dir('correct.scss', CORRECT_SCSS)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            SCSSLint(self.options).run()
        with open(os.path.join(parts_dir, 'scsslint.xml')) as fh:
            warnings = fh.read()
        rmtree(parts_dir)
        self.assertTrue(warnings.startswith('<?xml'))
        self.assertTrue('<checkstyle ' in warnings)
        self.assertFalse('<error ' in warnings)

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_file_contains_xml_when_jenkins_without_scss(self):
        # should output even in the absence of scss files to check
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            returnvalue = SCSSLint(self.options).run()
        with open(os.path.join(parts_dir, 'scsslint.xml')) as fh:
            warnings = fh.read()
        rmtree(parts_dir)
        self.assertTrue(returnvalue)
        self.assertTrue(warnings.startswith('<?xml'))
        self.assertTrue('<checkstyle ' in warnings)
        self.assertFalse('<error ' in warnings)


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
        rmtree(parts_dir)
        self.assertTrue(warnings.startswith('<?xml'))
        self.assertIn('<error', warnings)
        self.assertIn('line="2"', warnings)
        self.assertIn('severity="warning"', warnings)
        self.assertIn('Line should be indented 2 spaces', warnings)

    def test_parse_output(self):
        self.given_a_file_in_test_dir('correct.scss', CORRECT_SCSS)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with open(os.path.join(parts_dir, 'scsslint.xml'), 'w+') as fh:
            fh.write(RUBY_DEPRECATED_XML)
            fh.seek(0)
            linter = SCSSLint(self.options)
            with OutputCapture():
                linter.parse_output(fh, True)
        with open(os.path.join(parts_dir, 'scsslint.xml'), 'r') as fh:
            warnings = fh.read()
        rmtree(parts_dir)
        self.assertNotIn('DEPRECATION', warnings)
        self.assertTrue(warnings.startswith('<?xml'))
        # make sure we have no dangling repeated lines
        linecount = len([x for x in warnings.split('\n') if x])
        self.assertEqual(6, linecount)

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('correct.scss', CORRECT_SCSS)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    @unittest.skipIf(not SCSSLINT_INSTALLED, SCSSLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('incorrect.scss', INCORRECT_SCSS)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
