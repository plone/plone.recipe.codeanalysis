# -*- coding: utf-8 -*-
import unittest
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from mock import MagicMock
from mock import patch


class TestJSHint(unittest.TestCase):
    @patch('subprocess.Popen')
    def test_analysis_should_return_false(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x (E000) x ', 'IGNORED ERR',)
        )
        from subprocess import Popen  # noqa
        options = {'jshint-bin': 'FAKE_EXECUTABLE',
                   'jshint-exclude': 'FAKE_EXCLUDE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertFalse(code_analysis_jshint(options))

    @patch('subprocess.Popen')
    def test_analysis_should_return_true(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x (W000) x ', 'IGNORED ERR',)
        )
        from subprocess import Popen  # noqa
        options = {'jshint-bin': 'FAKE_EXECUTABLE',
                   'jshint-exclude': 'FAKE_EXCLUDE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertTrue(code_analysis_jshint(options))
