# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.flake8 import code_analysis_flake8
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase


class TestFlake8(TestCase):
    def setUp(self):
        self.options = {
            'bin-directory': 'bin/',
            'flake8-ignore': '',
            'flake8-exclude': 'bootstrap.py,bootstrap-buildout.py,docs,*.egg',
            'flake8-max-complexity': '10',
            'flake8-max-line-length': '79',
            'jenkins': 'False'
        }
        if path_isfile('../../bin/flake8'):  # when cwd is parts/test
            self.options['bin-directory'] = '../../bin/'
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        incorrect_code = open(path_join(self.test_dir, 'incorrect.py'), 'w')
        incorrect_code.write(
            'import sys\n'
            'class MyClass():\n'
            '    def __init__(self):\n'
            '        my_sum=1+1')  # No space between operators.
        incorrect_code.close()
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_flake8(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so it should raise an OSError
        # and return false.
        self.options['bin-directory'] = 'FAKE_DIR'
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_flake8(self.options))

    def test_analysis_should_return_true(self):
        correct_code = open(path_join(self.test_dir, 'correct.py'), 'w')
        correct_code.write(
            'class MyClass():\n'
            '    def __init__(self):\n'
            '        my_sum = 1 + 1\n'
            '        self.my_sum = my_sum\n')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_flake8(self.options))

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        correct_code = open(path_join(self.test_dir, 'correct.py'), 'w')
        correct_code.write(
            'class MyClass():\n'
            '    def __init__(self):\n'
            '        my_sum = 1 + 1\n'
            '        self.my_sum = my_sum\n')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_flake8(self.options)
        file_exist = path_isfile(path_join(location_tmp_dir, 'flake8.log'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)
