# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from plone.recipe.codeanalysis.jscs import JSCS
from plone.recipe.codeanalysis.jscs import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import TemporaryFile
from tempfile import mkdtemp
import os

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


class TestJavascriptCodeStyleChecker(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestJavascriptCodeStyleChecker, self).setUp()
        self.options.update({
            'jscs-bin': 'bin/jscs',
            'jscs-exclude': '',
        })
        if os.path.isfile('../../bin/jscs'):  # when cwd is parts/test
            self.options['jscs-bin'] = '../../bin/jscs'

    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('incorrect.js', INCORRECT_FILE)
        self.assertFalse(JSCS(self.options).run())

    def test_analysis_should_return_true_when_invalid_file_is_excluded(self):
        filename = 'incorrect.js'
        self.given_a_file_in_test_dir(filename, INCORRECT_FILE)
        self.options['jscs-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(JSCS(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        self.given_a_file_in_test_dir('incorrect.js', INCORRECT_FILE)
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['jscs-bin'] = 'FAKE_BIN'
        self.assertTrue(JSCS(self.options).run())

    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('correct.js', CORRECT_FILE)
        self.assertTrue(JSCS(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        parts_dir = mkdtemp()
        self.given_a_file_in_test_dir('correct.js', CORRECT_FILE)
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        JSCS(self.options).run()
        file_exist = os.path.isfile(os.path.join(parts_dir, 'jscs.xml'))
        rmtree(parts_dir)
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

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('incorrect.js', INCORRECT_FILE)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
