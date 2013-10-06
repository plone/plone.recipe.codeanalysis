# -*- utf-8 -*-

import unittest
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from mock import Mock
import subprocess


class TestJSHint(unittest.TestCase):
    def test_analysis_should_return_false(self):
        class Process(object):
            def communicate(self):
                return ' x (E000) x ', 'IGNORED ERR'
        subprocess.Popen = Mock(return_value=Process())
        options = {'jshint-bin': 'FAKE_EXECUTABLE',
                   'jshint-exclude': 'FAKE_EXCLUDE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False',
        }
        self.assertFalse(code_analysis_jshint(options))

    def test_analysis_should_return_true(self):
        class Process(object):
            def communicate(self):
                return ' x (W000) x ', 'IGNORED ERR'
        subprocess.Popen = Mock(return_value=Process())
        options = {'jshint-bin': 'FAKE_EXECUTABLE',
                   'jshint-exclude': 'FAKE_EXCLUDE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False',
        }
        self.assertTrue(code_analysis_jshint(options))