# -*- utf-8 -*-

import unittest
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from mock import Mock
import subprocess


class TestCssLint(unittest.TestCase):
    def test_analysis_should_return_false(self):
        class Process(object):
            def communicate(self):
                return ' x Error - x ', 'IGNORED ERR'
        subprocess.Popen = Mock(return_value=Process())
        options = {'csslint-bin': 'FAKE_EXECUTABLE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertFalse(code_analysis_csslint(options))

    def test_analysis_should_return_true(self):
        class Process(object):
            def communicate(self):
                return ' x (W000) x ', 'IGNORED ERR'
        subprocess.Popen = Mock(return_value=Process())
        options = {'csslint-bin': 'FAKE_EXECUTABLE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertTrue(code_analysis_csslint(options))
