# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.jshint import JSHint
from shutil import rmtree
from tempfile import TemporaryFile
from tempfile import mkdtemp
import unittest

INCORRECT_FILE = """var number_ten= =10;
var word_ten='ten';
var sum_2_plus_2 = 2+2;
"""

CORRECT_FILE = """var number_ten=10;
var word_ten='ten';
var sum_2_plus_2 = 2+2;
"""

WARNINGS_FILE = """function slideJump() {
    if (window.location.hash == null ||
        window.location.hash == '') {
            return;
        }
    if (window.location.hash == null) return;
    if (dest == null) {
        dest = 0;
    }
}
"""

EXPECTED_WARNINGS_OUTPUT = """{0[directory]}/warnings.js: line 2, col 30, Use '===' to compare with 'null'. (W041)
{0[directory]}/warnings.js: line 3, col 30, Use '===' to compare with ''. (W041)
{0[directory]}/warnings.js: line 6, col 30, Use '===' to compare with 'null'. (W041)
{0[directory]}/warnings.js: line 7, col 14, Use '===' to compare with 'null'. (W041)

4 errors
"""  # noqa

XML_EMPTY_OUTPUT = """<?xml version="1.0" encoding="utf-8"?>
<jslint>
</jslint>"""

XML_OUTPUT = """<?xml version="1.0" encoding="utf-8"?>
<jslint>
    <file name="incorrect.js">
        <issue line="1" char="17" reason="Expected an identifier and instead saw &apos;=&apos;." evidence="var number_ten= =10;var word_ten=&apos;ten&apos;;var sum_2_plus_2 = 2+2;" severity="E" />
        <issue line="1" char="18" reason="Missing semicolon." evidence="var number_ten= =10;var word_ten=&apos;ten&apos;;var sum_2_plus_2 = 2+2;" severity="W" />
        <issue line="1" char="18" reason="Expected an assignment or function call and instead saw an expression." evidence="var number_ten= =10;var word_ten=&apos;ten&apos;;var sum_2_plus_2 = 2+2;" severity="W" />
    </file>
</jslint>"""  # noqa

DEFAULT_OUTPUT = """incorrect.js: line 1, col 17, Expected an identifier and instead saw '='. (E030)
incorrect.js: line 1, col 18, Missing semicolon. (W033)
incorrect.js: line 1, col 18, Expected an assignment or function call and instead saw an expression. (W030)

3 errors
"""  # noqa


class TestJSHint(unittest.TestCase):

    def setUp(self):  # noqa
        self.options = {
            'jshint-bin': 'bin/jshint',
            'jshint-exclude': '',
            'jenkins': 'False'
        }
        if path_isfile('../../bin/jshint'):  # when cwd is parts/test
            self.options['jshint-bin'] = '../../bin/jshint'

        self.test_dir = mkdtemp()

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        full_path = path_join(self.test_dir, 'incorrect.js')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertFalse(JSHint(self.options).run())

    def test_analysis_should_return_true_for_warnings(self):
        full_path = path_join(self.test_dir, 'warnings.js')
        with open(full_path, 'w') as warnings_code:
            warnings_code.write(WARNINGS_FILE)
        self.options['directory'] = self.test_dir
        self.assertTrue(JSHint(self.options).run())

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # and return false.
        self.options['jshint-bin'] = 'FAKE_BIN'
        self.options['directory'] = 'FAKE_DIR'
        self.assertFalse(JSHint(self.options).run())

    def test_analysis_should_return_true(self):
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertTrue(JSHint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        JSHint(self.options).run()
        file_exist = path_isfile(path_join(location_tmp_dir, 'jshint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_jshint_parse_output_should_return_true_empty_xml_output(self):
        jshint_file = TemporaryFile('w+')
        jshint_file.write(XML_EMPTY_OUTPUT)
        jshint_file.seek(0)
        self.options['jenkins'] = 'True'
        linter = JSHint(self.options)
        self.assertTrue(linter.use_jenkins)
        self.assertTrue(linter.parse_output(jshint_file, 1))

    def test_jshint_parse_output_should_return_false_with_xml_output(self):
        jshint_file = TemporaryFile('w+')
        jshint_file.write(XML_OUTPUT)
        jshint_file.seek(0)
        self.options['jenkins'] = 'True'
        linter = JSHint(self.options)
        self.assertTrue(linter.use_jenkins)
        self.assertFalse(linter.parse_output(jshint_file, 1))

    def test_jshint_parse_output_should_return_false_with_normal_output(self):
        jshint_file = TemporaryFile('w+')
        jshint_file.write(DEFAULT_OUTPUT)
        jshint_file.seek(0)
        self.options['jenkins'] = 'False'
        linter = JSHint(self.options)
        self.assertFalse(linter.use_jenkins)
        self.assertFalse(linter.parse_output(jshint_file, 1))

    def test_jshint_parse_output_should_return_true_empty_normal_output(self):
        jshint_file = TemporaryFile('w+')
        jshint_file.write('')
        jshint_file.seek(0)
        self.options['jenkins'] = 'False'
        linter = JSHint(self.options)
        self.assertFalse(linter.use_jenkins)
        self.assertTrue(linter.parse_output(jshint_file, 1))
