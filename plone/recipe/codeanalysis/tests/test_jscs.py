# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.jscs import code_analysis_jscs
from plone.recipe.codeanalysis.jscs import jscs_errors
from shutil import rmtree
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

    def setUp(self):
        self.options = {
            'jscs-bin': 'bin/jscs',
            'jscs-exclude': '',
            'jenkins': 'False'
        }
        if path_isfile('../../bin/jscs'):  # when cwd is parts/test
            self.options['jscs-bin'] = '../../bin/jscs'
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        full_path = path_join(self.test_dir, 'incorrect.js')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_jscs(self.options))

    def test_analysis_should_return_true_when_invalid_file_is_excluded(self):
        full_path = path_join(self.test_dir, 'incorrect.js')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['jscs-exclude'] = full_path
        self.assertTrue(code_analysis_jscs(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # and return false.
        self.options['jscs-bin'] = 'FAKE_BIN'
        self.options['directory'] = 'FAKE_DIR'
        self.assertFalse(code_analysis_jscs(self.options))

    def test_analysis_should_return_true(self):
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_jscs(self.options))

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_jscs(self.options)
        file_exist = path_isfile(path_join(location_tmp_dir, 'jscs.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_jscs_errors_should_return_false_empty_xml_output(self):
        self.assertFalse(jscs_errors(XML_EMPTY_OUTPUT, True))

    def test_jscs_errors_should_return_true_with_xml_output(self):
        self.assertTrue(jscs_errors(XML_OUTPUT, True))

    def test_jscs_errors_should_return_true_with_normal_output(self):
        self.assertTrue(jscs_errors(DEFAULT_OUTPUT, False))

    def test_jscs_errors_should_return_false_empty_normal_output(self):
        self.assertFalse(jscs_errors('', False))
