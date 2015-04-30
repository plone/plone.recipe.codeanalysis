# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.jscs import JSCS
from shutil import rmtree
from tempfile import TemporaryFile
from tempfile import mkdtemp
import unittest

INCORRECT_FILE = """\
function a_method(){
  if(window.location.hash == null) return
}
"""

CORRECT_FILE = """\
function slideJump() {
  if (window.location.hash === null) {
    return;
  }
}
"""

XML_EMPTY_OUTPUT = """\
<?xml version="1.0" encoding="utf-8"?>
<checkstyle version="4.3">
    <file name="test.js">
    </file>
</checkstyle>"""

XML_OUTPUT = """\
<?xml version="1.0" encoding="utf-8"?>
<checkstyle version="4.3">
    <file name="test.js">
        <error line="1" column="10" severity="error" message="All identifiers must be camelCase or UPPER_CASE" source="jscs" />
        <error line="1" column="19" severity="error" message="Missing space before opening curly brace" source="jscs" />
    </file>
</checkstyle>"""  # noqa

DEFAULT_OUTPUT = """\
All identifiers must be camelCase or UPPER_CASE at /tmp/tmp679DaV/incorrect.js :
     1 |function a_method(){
-----------------^
     2 |  if(window.location.hash == null) return
     3 |}

Missing space before opening curly brace at /tmp/tmp679DaV/incorrect.js :
     1 |function a_method(){
--------------------------^
     2 |  if(window.location.hash == null) return
     3 |}


2 code style errors found.
"""  # noqa


class TestJavascriptCodeStyleChecker(unittest.TestCase):

    def setUp(self):  # noqa
        self.options = {
            'jscs-bin': 'bin/jscs',
            'jscs-exclude': '',
            'jenkins': 'False'
        }
        if path_isfile('../../bin/jscs'):  # when cwd is parts/test
            self.options['jscs-bin'] = '../../bin/jscs'
        self.test_dir = mkdtemp()

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        full_path = path_join(self.test_dir, 'incorrect.js')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertFalse(JSCS(self.options).run())

    def test_analysis_should_return_true_when_invalid_file_is_excluded(self):
        full_path = path_join(self.test_dir, 'incorrect.js')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['jscs-exclude'] = full_path
        self.assertTrue(JSCS(self.options).run())

    def test_analysis_should_return_false_when_oserror(self):
        full_path = path_join(self.test_dir, 'incorrect.js')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        # The options are fake, so the function should raise an OSError
        # and return false.
        self.options['jscs-bin'] = 'FAKE_BIN'
        self.assertFalse(JSCS(self.options).run())

    def test_analysis_should_return_true(self):
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertTrue(JSCS(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        JSCS(self.options).run()
        file_exist = path_isfile(path_join(location_tmp_dir, 'jscs.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_jscs_parse_output_should_return_true_empty_xml_output(self):
        jscs_file = TemporaryFile('w+')
        jscs_file.write(XML_EMPTY_OUTPUT)
        jscs_file.seek(0)
        self.options['jenkins'] = 'True'
        linter = JSCS(self.options)
        self.assertTrue(linter.use_jenkins)
        self.assertTrue(linter.parse_output(jscs_file, 1))

    def test_jscs_parse_output_should_return_false_with_xml_output(self):
        jscs_file = TemporaryFile('w+')
        jscs_file.write(XML_OUTPUT)
        jscs_file.seek(0)
        self.options['jenkins'] = 'True'
        linter = JSCS(self.options)
        self.assertTrue(linter.use_jenkins)
        self.assertFalse(linter.parse_output(jscs_file, 1))

    def test_jscs_parse_output_should_return_false_with_normal_output(self):
        jscs_file = TemporaryFile('w+')
        jscs_file.write(DEFAULT_OUTPUT)
        jscs_file.seek(0)
        self.options['jenkins'] = 'False'
        linter = JSCS(self.options)
        self.assertFalse(linter.use_jenkins)
        self.assertFalse(linter.parse_output(jscs_file, 1))

    def test_jscs_parse_output_should_return_true_empty_normal_output(self):
        jscs_file = TemporaryFile('w+')
        jscs_file.write('')
        jscs_file.seek(0)
        self.options['jenkins'] = 'False'
        linter = JSCS(self.options)
        self.assertFalse(linter.use_jenkins)
        self.assertTrue(linter.parse_output(jscs_file, 1))
