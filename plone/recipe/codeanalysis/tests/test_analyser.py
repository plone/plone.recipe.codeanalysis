# -*- coding: utf-8 -*-
from unittest import TestCase
from plone.recipe.codeanalysis.analyser import Analyser


class TestCssLint(TestCase):
    def setUp(self):
        self.options = {
            'bin': 'echo',
            'directory': '/tmp/',
            'jenkins': 'False'
        }
        self.analysis = Analyser(options=self.options)

    def tearDown(self):
        if self.analysis.output_file:
            self.analysis.output_file.close()

    def test_analysis_run(self):
        expected_output = 'some_arg /tmp/\n'
        actual_output = self.analysis.run()
        self.assertEqual(expected_output, actual_output)

    def test_cmd_property(self):
        expected_cmd = ['echo', 'some_arg', '/tmp/']
        actual_cmd = self.analysis.cmd
        self.assertEqual(expected_cmd, actual_cmd)

    def test_normalize_boolean_should_return_true(self):
        actual_value = self.analysis.normalize_boolean('True')
        self.assertTrue(actual_value)
        actual_value = self.analysis.normalize_boolean('true')
        self.assertTrue(actual_value)

    def test_get_jenkins_output_filename(self):
        actual_value = self.analysis.jenkins_output_fullpath
        self.assertEqual('analysis.xml', actual_value)

    def test_normalise_boolean_should_return_false(self):
        actual_value = self.analysis.normalize_boolean('False')
        self.assertFalse(actual_value)
        actual_value = self.analysis.normalize_boolean('false')
        self.assertFalse(actual_value)

    def test_use_jenkins_should_be_false(self):
        self.analysis.options['jenkins'] = 'False'
        self.assertFalse(self.analysis.use_jenkins)

    def test_use_jenkins_should_be_true(self):
        self.analysis.options['jenkins'] = 'True'
        self.assertTrue(self.analysis.use_jenkins)

    def test_file_should_be_opened(self):
        self.analysis.open_output_file()
        self.assertFalse(self.analysis.output_file.closed)
