# -*- coding: utf-8 -*-
import unittest
from plone.recipe.codeanalysis.flake8 import code_analysis_flake8
from mock import MagicMock
from mock import patch
from mock import PropertyMock


class TestFlake8(unittest.TestCase):
    @patch('subprocess.Popen')
    def test_analysis_should_return_false(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x Error should return false x ', 'IGNORED ERR',)
        )
        returncode = PropertyMock(return_value=1)
        type(mock_class()).returncode = returncode
        from subprocess import Popen  # noqa
        options = {
            'bin-directory': 'FAKE_BIN_DIRECTORY',
            'flake8-ignore': 'FAKE_IGNORE',
            'flake8-exclude': 'FAKE_EXCLUDE',
            'flake8-max-complexity': 'FAKE_MAX_COMPLEXITY',
            'flake8-max-line-length': 'FAKE_MAX_LENGTH',
            'directory': 'FAKE_DIRECTORY',
            'jenkins': 'False',
        }
        self.assertFalse(code_analysis_flake8(options))

    @patch('subprocess.Popen')
    def test_analysis_should_return_true(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x ok, should return true x ', 'IGNORED ERR',)
        )
        returncode = PropertyMock(return_value=0)
        type(mock_class()).returncode = returncode
        from subprocess import Popen  # noqa
        options = {
            'bin-directory': 'FAKE_BIN_DIRECTORY',
            'flake8-ignore': 'FAKE_IGNORE',
            'flake8-exclude': 'FAKE_EXCLUDE',
            'flake8-max-complexity': 'FAKE_MAX_COMPLEXITY',
            'flake8-max-line-length': 'FAKE_MAX_LENGTH',
            'directory': 'FAKE_DIRECTORY',
            'jenkins': 'False',
        }
        self.assertTrue(code_analysis_flake8(options))
