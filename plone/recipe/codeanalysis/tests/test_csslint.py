# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from plone.recipe.codeanalysis.csslint import csslint_errors
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase


class TestCssLint(TestCase):
    def setUp(self):
        self.options = {
            'csslint-bin': 'bin/csslint',
            'jenkins': 'False'
        }
        if path_isfile('../../bin/csslint'):  # when cwd is parts/test
            self.options['csslint-bin'] = '../../bin/csslint'
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        incorrect_code = open(path_join(self.test_dir, 'incorrect.css'), 'w')
        incorrect_code.write(
            'a:link {color: blue}\n'
            '{}\n'
            'h3 {color: red}\n'
            'bodyy {color: purple}')
        incorrect_code.close()
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_csslint(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so it should raise an OSError
        # and return false.
        self.options['csslint-bin'] = 'FAKE_BIN'
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_csslint(self.options))

    def test_analysis_should_return_true(self):
        correct_code = open(path_join(self.test_dir, 'correct.css'), 'w')
        correct_code.write(
            'a:link {color:blue}\n'
            'h3 {color: red}\n'
            'body {color: purple}')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_csslint(self.options))

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        correct_code = open(path_join(self.test_dir, 'correct.css'), 'w')
        correct_code.write(
            'a:link {color:blue}\n'
            'h3 {color: red}\n'
            'body {color: purple}')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_csslint(self.options)
        file_exist = path_isfile(path_join(location_tmp_dir, 'csslint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_jshint_errors_should_return_false_xml_output(self):
        output = '<?xml version="1.0" encoding="utf-8"?><lint>\n</lint>\n'
        self.assertFalse(csslint_errors(output, True))

    def test_jshint_errors_should_return_true_xml_output(self):
        output = '<?xml version="1.0" encoding="utf-8"?><lint>\n<file name='\
            '"incorrect.css"><issue line="2" char="1" severity="error" '\
            'reason="Unexpected token \'{\' at line 2, col 1." evidence='\
            '"{}"/><issue line="2" char="2" severity="error" '\
            'reason="Unexpected token \'}\' at line 2, col 2." evidence='\
            '"{}"/></file>\n</lint>\n'
        self.assertTrue(csslint_errors(output, True))

    def test_jshint_errors_should_return_true_normal_output(self):
        output = 'incorrect.css: line 2, col 1, Error - Unexpected token '\
            '\'{\' at line 2, col 1.\nincorrect.css: line 2, col 2, Error'\
            ' - Unexpected token \'}\' at line 2, col 2.\n\n'
        self.assertTrue(csslint_errors(output, False))

    def test_jshint_errors_should_return_false_normal_output(self):
        output = ''
        self.assertFalse(csslint_errors(output, False))
