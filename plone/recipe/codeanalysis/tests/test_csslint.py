# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.csslint import CSSLint
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase

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


class TestCssLint(TestCase):

    def setUp(self):  # noqa
        self.test_dir = mkdtemp()
        self.options = {
            'csslint-bin': 'bin/csslint',
            'jenkins': 'False',
            'directory': self.test_dir
        }
        if path_isfile('../../bin/csslint'):  # when cwd is parts/test
            self.options['csslint-bin'] = '../../bin/csslint'
        # Create a valid file for each testcase
        with open(path_join(self.test_dir, 'correct.css'), 'w') as f:
            f.write(CORRECT_CSS)

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        with open(path_join(self.test_dir, 'incorrect.css'), 'w') as f:
            f.write(INCORRECT_CSS)
        self.assertFalse(CSSLint(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['csslint-bin'] = 'FAKE_BIN'
        self.assertTrue(CSSLint(self.options).run())

    def test_analysis_should_return_true(self):
        self.assertTrue(CSSLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        CSSLint(self.options).run()
        file_exist = path_isfile(path_join(location_tmp_dir, 'csslint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)
