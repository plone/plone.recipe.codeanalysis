# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from plone.recipe.codeanalysis.csslint import CSSLint
from plone.recipe.codeanalysis.csslint import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
import os

CORRECT_CSS = """\
a:link {color:blue}
h3 {color: red}
body {color: purple}
"""

INCORRECT_CSS = """\
a:link {color: blue}
{}
h3 {color: red}
bodyy {color: purple}
"""


class TestCSSLint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestCSSLint, self).setUp()
        self.options.update({
            'csslint-bin': 'bin/csslint',
        })
        if os.path.isfile('../../bin/csslint'):  # when cwd is parts/test
            self.options['csslint-bin'] = '../../bin/csslint'

        self.given_a_file_in_test_dir('correct.css', CORRECT_CSS)

    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('incorrect.css', INCORRECT_CSS)
        self.assertFalse(CSSLint(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['csslint-bin'] = 'FAKE_BIN'
        self.assertTrue(CSSLint(self.options).run())

    def test_analysis_should_return_true(self):
        self.assertTrue(CSSLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        CSSLint(self.options).run()
        file_exist = os.path.isfile(os.path.join(parts_dir, 'csslint.xml'))
        rmtree(parts_dir)
        self.assertTrue(file_exist)

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('incorrect.css', INCORRECT_CSS)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
