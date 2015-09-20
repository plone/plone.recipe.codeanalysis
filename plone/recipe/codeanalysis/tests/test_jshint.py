# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.jshint import console_script
from plone.recipe.codeanalysis.jshint import JSHint
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture


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


class TestJSHint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestJSHint, self).setUp()
        self.options.update({
            'jshint-bin': 'bin/jshint',
            'jshint-exclude': '',
            'jshint-suppress-warnings': 'True',
            'jenkins': 'False',
            'directory': self.test_dir,
        })
        if path_isfile('../../bin/jshint'):  # when cwd is parts/test
            self.options['jshint-bin'] = '../../bin/jshint'
        self.given_a_file_in_test_dir('correct.js', CORRECT_FILE)

    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('incorrect.js', INCORRECT_FILE)
        with OutputCapture():
            self.assertFalse(JSHint(self.options).run())

    def test_analysis_should_return_true_for_warnings(self):
        self.given_a_file_in_test_dir('warnings.js', WARNINGS_FILE)
        with OutputCapture():
            self.assertTrue(JSHint(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['jshint-bin'] = 'FAKE_BIN'
        with OutputCapture():
            self.assertTrue(JSHint(self.options).run())

    def test_analysis_should_return_true(self):
        with OutputCapture():
            self.assertTrue(JSHint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            JSHint(self.options).run()
        file_exist = path_isfile(path_join(location_tmp_dir, 'jshint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_jshint_parse_output_should_return_true_empty_xml_output(self):
        file_path = self.given_a_file_in_test_dir(
            'jshint.xml',
            XML_EMPTY_OUTPUT
        )
        self.options['jenkins'] = 'True'
        linter = JSHint(self.options)
        self.assertTrue(linter.use_jenkins)
        with OutputCapture():
            self.assertTrue(linter.parse_output(open(file_path), 1))

    def test_jshint_parse_output_should_return_false_with_xml_output(self):
        file_path = self.given_a_file_in_test_dir('jshint.xml', XML_OUTPUT)
        self.options['jenkins'] = 'True'
        linter = JSHint(self.options)
        self.assertTrue(linter.use_jenkins)
        with OutputCapture():
            self.assertFalse(linter.parse_output(open(file_path), 1))

    def test_jshint_parse_output_should_return_false_with_normal_output(self):
        file_path = self.given_a_file_in_test_dir('jshint.xml', DEFAULT_OUTPUT)
        self.options['jenkins'] = 'False'
        linter = JSHint(self.options)
        self.assertFalse(linter.use_jenkins)
        with OutputCapture():
            self.assertFalse(linter.parse_output(open(file_path), 1))

    def test_jshint_parse_output_should_return_true_empty_normal_output(self):
        file_path = self.given_a_file_in_test_dir('jshint.xml', '')
        self.options['jenkins'] = 'False'
        linter = JSHint(self.options)
        self.assertFalse(linter.use_jenkins)
        with OutputCapture():
            self.assertTrue(linter.parse_output(open(file_path), 1))

    def test_jshint_parse_output_should_return_false_if_warnings_not_suppressed(self):  # noqa
        file_path = self.given_a_file_in_test_dir(
            'jshint.xml',
            EXPECTED_WARNINGS_OUTPUT
        )
        self.options['jenkins'] = 'False'
        self.options['jshint-suppress-warnings'] = 'False'
        linter = JSHint(self.options)
        self.assertFalse(linter.use_jenkins)
        with OutputCapture():
            self.assertFalse(linter.parse_output(open(file_path), 1))

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('incorrect.js', INCORRECT_FILE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
