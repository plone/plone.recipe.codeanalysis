# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from plone.recipe.codeanalysis.jshint import jshint_errors
from plone.recipe.codeanalysis.jshint import run_cmd
from shutil import rmtree
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
    def setUp(self):
        self.options = {
            'jshint-bin': 'bin/jshint',
            'jshint-exclude': '',
            'jenkins': 'False'
        }
        if path_isfile('../../bin/jshint'):  # when cwd is parts/test
            self.options['jshint-bin'] = '../../bin/jshint'

        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        full_path = path_join(self.test_dir, 'incorrect.js')
        with open(full_path, 'w') as incorrect_code:
            incorrect_code.write(INCORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_jshint(self.options))

    def test_analysis_should_output_warnings(self):
        full_path = path_join(self.test_dir, 'warnings.js')
        with open(full_path, 'w') as warnings_code:
            warnings_code.write(WARNINGS_FILE)
        self.options['directory'] = self.test_dir
        expected_output = EXPECTED_WARNINGS_OUTPUT.format(self.options)
        output = run_cmd(self.options, False)
        self.assertEqual(output, expected_output)

    def test_analysis_should_return_true_for_warnings(self):
        full_path = path_join(self.test_dir, 'warnings.js')
        with open(full_path, 'w') as warnings_code:
            warnings_code.write(WARNINGS_FILE)
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_jshint(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # and return false.
        self.options['jshint-bin'] = 'FAKE_BIN'
        self.options['directory'] = 'FAKE_DIR'
        self.assertFalse(code_analysis_jshint(self.options))

    def test_analysis_should_return_true(self):
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_jshint(self.options))

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        full_path = path_join(self.test_dir, 'correct.js')
        with open(full_path, 'w') as correct_code:
            correct_code.write(CORRECT_FILE)
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_jshint(self.options)
        file_exist = path_isfile(path_join(location_tmp_dir, 'jshint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_jshint_errors_should_return_false_empty_xml_output(self):
        self.assertFalse(jshint_errors(XML_EMPTY_OUTPUT, True))

    def test_jshint_errors_should_return_true_with_xml_output(self):
        self.assertTrue(jshint_errors(XML_OUTPUT, True))

    def test_jshint_errors_should_return_true_with_normal_output(self):
        self.assertTrue(jshint_errors(DEFAULT_OUTPUT, False))

    def test_jshint_errors_should_return_false_empty_normal_output(self):
        self.assertFalse(jshint_errors('', False))
