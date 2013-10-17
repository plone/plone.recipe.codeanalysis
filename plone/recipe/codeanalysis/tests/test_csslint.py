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
    def setUp(self):
        self.options = {
            'csslint-bin': 'FAKE_EXECUTABLE',
            'directory': 'FAKE_DIRECTORY',
            'jenkins': 'False'
        }

    def test_analysis_should_return_false_when_exception_occurs(self):
        # The options are fake, so it should raise an OSError
        # and return false.
        self.assertFalse(code_analysis_csslint(self.options))

    # TODO: communicate method is not called any more,
    # need to rewrite this test.
    #@patch('subprocess.Popen')
    #def test_analysis_should_return_false_when_error_found(self, mock_class):
    #    mock_class().communicate = MagicMock(
    #        return_value=(' x Error - x ', 'IGNORED ERR',)
    #    )
    #    self.assertFalse(code_analysis_csslint(self.options))

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
        code_analysis_csslint(self.options)
        file_exist = path_isfile(path_join(tmp_dir, 'csslint.xml'))
        rmtree(tmp_dir)
        self.assertTrue(file_exist)

    @patch('subprocess.Popen')
    def test_analysis_should_return_true(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x no error x ', 'IGNORED ERR',)
        )
        self.assertTrue(code_analysis_csslint(self.options))
