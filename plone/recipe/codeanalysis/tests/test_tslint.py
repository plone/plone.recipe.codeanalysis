# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.tslint import TSLint
from shutil import rmtree
from tempfile import TemporaryFile
from tempfile import mkdtemp
import unittest

INCORRECT_FILE = """\
declare module a {
    module route {
        interface b {
            c: string;
        }
    }
}"""

CORRECT_FILE = """\
declare module a {
    module route {
        interface b {
            c: string;
        }
    }
}
"""
JSON_EMPTY_OUTPUT = """\
{}"""

DEFAULT_OUTPUT = """\
{}"""

JSON_OUTPUT = """\
{}"""


class TestTypeScriptStyleChecker(unittest.TestCase):

    def setUp(self):
        self.options = {
            'tslint-bin': 'bin/tslint',
            'tslint-exclude': '',
            'jenkins': 'False'
        }
        if path_isfile('../../bin/tslint'):  # when cwd is parts/test
            self.options['tslint-bin'] = '../../bin/tslint'
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        full_path = path_join(self.test_dir, 'incorrect.ts')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertFalse(TSLint(self.options).run())

    def test_analysis_should_return_true_when_invalid_file_is_excluded(self):
        full_path = path_join(self.test_dir, 'incorrect.ts')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['tslint-exclude'] = full_path
        self.assertTrue(TSLint(self.options).run())

    def test_analysis_should_return_false_when_oserror(self):
        full_path = path_join(self.test_dir, 'incorrect.ts')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        # The options are fake, so the function should raise an OSError
        # and return false.
        self.options['tslint-bin'] = 'FAKE_BIN'
        self.assertFalse(TSLint(self.options).run())

    def test_analysis_should_return_true(self):
        full_path = path_join(self.test_dir, 'correct.ts')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertTrue(TSLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        full_path = path_join(self.test_dir, 'correct.ts')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        TSLint(self.options).run()
        file_exist = path_isfile(path_join(location_tmp_dir, 'tslint.json'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_tslint_parse_output_should_return_true_empty_xml_output(self):
        tslint_file = TemporaryFile('w+')
        tslint_file.write(JSON_EMPTY_OUTPUT)
        tslint_file.seek(0)
        self.options['jenkins'] = 'True'
        linter = TSLint(self.options)
        self.assertTrue(linter.use_jenkins)
        self.assertTrue(linter.parse_output(tslint_file, 1))

    def test_tslint_parse_output_should_return_false_with_xml_output(self):
        tslint_file = TemporaryFile('w+')
        tslint_file.write(JSON_OUTPUT)
        tslint_file.seek(0)
        self.options['jenkins'] = 'True'
        linter = TSLint(self.options)
        self.assertTrue(linter.use_jenkins)
        self.assertFalse(linter.parse_output(tslint_file, 1))

    def test_tslint_parse_output_should_return_false_with_normal_output(self):
        tslint_file = TemporaryFile('w+')
        tslint_file.write(DEFAULT_OUTPUT)
        tslint_file.seek(0)
        self.options['jenkins'] = 'False'
        linter = TSLint(self.options)
        self.assertFalse(linter.use_jenkins)
        self.assertFalse(linter.parse_output(tslint_file, 1))

    def test_tslint_parse_output_should_return_true_empty_normal_output(self):
        tslint_file = TemporaryFile('w+')
        tslint_file.write('')
        tslint_file.seek(0)
        self.options['jenkins'] = 'False'
        linter = TSLint(self.options)
        self.assertFalse(linter.use_jenkins)
        self.assertTrue(linter.parse_output(tslint_file, 1))
