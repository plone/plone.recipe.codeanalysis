# -*- coding: utf-8 -*-
import os
import unittest
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from shutil import rmtree
from tempfile import mkdtemp
from os.path import join as path_join
from os.path import isfile as path_isfile


class TestJSHint(unittest.TestCase):
    def setUp(self):
        self.options = {
            'jshint-bin': 'jshint',
            'jshint-exclude': '',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        incorrect_code = file(path_join(self.test_dir, 'incorrect.js'), 'w')
        incorrect_code.write(
            'var number_ten= =10;'
            'var word_ten=\'ten\';'
            'var sum_2_plus_2 = 2+2;')
        incorrect_code.close()
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_jshint(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # and return false.
        self.options['jshint-bin'] = 'FAKE_BIN'
        self.options['directory'] = 'FAKE_DIR'
        self.assertFalse(code_analysis_jshint(self.options))

    def test_analysis_should_return_true(self):
        correct_code = file(path_join(self.test_dir, 'correct.js'), 'w')
        correct_code.write(
            'var number_ten=10;'
            'var word_ten=\'ten\';'
            'var sum_2_plus_2 = 2+2;')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_jshint(self.options))

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        correct_code = file(path_join(self.test_dir, 'correct.js'), 'w')
        correct_code.write(
            'var number_ten=10;'
            'var word_ten=\'ten\';'
            'var sum_2_plus_2 = 2+2;')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_jshint(self.options)
        file_exist = path_isfile(path_join(location_tmp_dir, 'jshint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)
