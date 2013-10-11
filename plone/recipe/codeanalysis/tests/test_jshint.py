# -*- coding: utf-8 -*-
import unittest
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from mock import MagicMock
from mock import patch
from shutil import rmtree
from tempfile import mkdtemp
from os.path import join as path_join
from os.path import isfile as path_isfile


class TestJSHint(unittest.TestCase):
    def setUp(self):
        self.options = {
            'jshint-bin': 'FAKE_EXECUTABLE',
            'jshint-exclude': 'FAKE_EXCLUDE',
            'directory': 'FAKE_DIRECTORY',
            'jenkins': 'False'
        }

    @patch('subprocess.Popen')
    def test_analysis_should_return_false_when_error_found(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x (E000) x ', 'IGNORED ERR',)
        )
        self.assertFalse(code_analysis_jshint(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so the function it should raise an OSError
        # and return false.
        self.assertFalse(code_analysis_jshint(self.options))

    @patch('subprocess.Popen')
    def test_analysis_should_return_true(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x (W000) x ', 'IGNORED ERR',)
        )
        self.assertTrue(code_analysis_jshint(self.options))

    @patch('subprocess.Popen')
    def test_analysis_file_should_exist_when_jenkins_is_true(self, mock_class):
        tmp_dir = mkdtemp()
        mock_class().communicate = MagicMock(
            return_value=(
                ' need to mock this, but the content doesn\'t matter ',
                'IGNORED ERR',)
        )
        self.options['location'] = tmp_dir
        self.options['jenkins'] = 'True' # need to activate jenkins.
        code_analysis_jshint(self.options)
        file_exist = path_isfile(path_join(tmp_dir, 'jshint.xml'))
        rmtree(tmp_dir)
        self.assertTrue(file_exist)
