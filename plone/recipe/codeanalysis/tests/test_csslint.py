# -*- coding: utf-8 -*-
import unittest
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from mock import MagicMock
from mock import patch


class TestCssLint(unittest.TestCase):
    def test_analysis_should_return_false_when_exception_occurs(self):
        options = {'csslint-bin': 'do_not_exist',
                   'directory': 'do_not_exist',
                   'jenkins': 'False'}
        self.assertFalse(code_analysis_csslint(options))

    @patch('subprocess.Popen')
    def test_analysis_should_return_false_when_error_found(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x Error - x ', 'IGNORED ERR',)
        )
        from subprocess import Popen  # noqa
        options = {'csslint-bin': 'FAKE_EXECUTABLE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertFalse(code_analysis_csslint(options))

    @patch('subprocess.Popen')
    def test_analysis_should_return_true(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x no error x ', 'IGNORED ERR',)
        )
        from subprocess import Popen  # noqa
        options = {'csslint-bin': 'FAKE_EXECUTABLE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertTrue(code_analysis_csslint(options))
