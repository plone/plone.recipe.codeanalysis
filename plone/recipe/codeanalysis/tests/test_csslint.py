# -*- coding: utf-8 -*-
from unittest import TestCase
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from mock import MagicMock
from mock import patch
from shutil import rmtree
from tempfile import mkdtemp
from os.path import join as path_join
from os.path import isfile as path_isfile


class TestCssLint(TestCase):
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
    def test_analysis_file_should_exist_when_jenkins_is_true(self, mock_class):
        tmp_dir = mkdtemp()
        mock_class().communicate = MagicMock(
            return_value=(' x Error - x ', 'IGNORED ERR',)
        )
        from subprocess import Popen  # noqa
        options = {'csslint-bin': 'FAKE_EXECUTABLE',
                   'directory': 'FAKE_DIRECTORY',
                   'location': tmp_dir,
                   'jenkins': 'True'}
        code_analysis_csslint(options)
        result = path_isfile(path_join(tmp_dir, 'csslint.xml'))
        rmtree(tmp_dir)
        self.assertTrue(result)

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
