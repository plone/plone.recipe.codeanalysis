# -*- coding: utf-8 -*-
from unittest import TestCase
from plone.recipe.codeanalysis.flake8 import code_analysis_flake8
from mock import MagicMock
from mock import patch
from mock import PropertyMock
from shutil import rmtree
from tempfile import mkdtemp
from os.path import join as path_join
from os.path import isfile as path_isfile


class TestFlake8(TestCase):
    def setUp(self):
        self.options = {
            'bin-directory': 'FAKE_BIN_DIRECTORY',
            'flake8-ignore': 'FAKE_IGNORE',
            'flake8-exclude': 'FAKE_EXCLUDE',
            'flake8-max-complexity': 'FAKE_MAX_COMPLEXITY',
            'flake8-max-line-length': 'FAKE_MAX_LENGTH',
            'directory': 'FAKE_DIRECTORY',
            'jenkins': 'False',
        }

    @patch('subprocess.Popen')
    def test_analysis_should_return_false_when_error_found(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x Error should return false x ', 'IGNORED ERR',)
        )
        returncode = PropertyMock(return_value=1)
        type(mock_class()).returncode = returncode
        self.assertFalse(code_analysis_flake8(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so it should raise an OSError
        # and return false.
        self.assertFalse(code_analysis_flake8(self.options))

    @patch('subprocess.Popen')
    def test_analysis_should_return_true(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x ok, should return true x ', 'IGNORED ERR',)
        )
        returncode = PropertyMock(return_value=0)
        type(mock_class()).returncode = returncode
        self.assertTrue(code_analysis_flake8(self.options))

    @patch('subprocess.Popen')
    def test_analysis_file_should_exist_when_jenkins_is_true(self, mock_class):
        tmp_dir = mkdtemp()
        mock_class().communicate = MagicMock(
            return_value=(
                ' need to mock this, but the content doesn\'t matter ',
                'IGNORED ERR',)
        )
        self.options['location'] = tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_flake8(self.options)
        file_exist = path_isfile(path_join(tmp_dir, 'flake8.log'))
        rmtree(tmp_dir)
        self.assertTrue(file_exist)
