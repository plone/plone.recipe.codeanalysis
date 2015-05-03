# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.debug_statements import DebugStatements
from plone.recipe.codeanalysis.debug_statements import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase

VALID_CODE = """\
def foo(bar):
    print('hello')  # noqa
"""

INVALID_CODE = """\
def foo(bar):
    print('hello')
"""

INVALID_JS = """\
function test() {
    console.log('hello world')
};
"""


class TestDebugStatements(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestDebugStatements, self).setUp()
        self.options.update({
            'debug-statements': 'True',
            'debug-statements-exclude': '',
        })

    def test_analysis_should_return_false_if_trailing_spaces_are_found(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        self.assertFalse(DebugStatements(self.options).run())

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self.given_a_file_in_test_dir(filename, INVALID_CODE)
        self.options['debug-statements-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(DebugStatements(self.options).run())

    def test_analysis_should_return_true_for_valid_files(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        self.assertTrue(DebugStatements(self.options).run())

    def test_analysis_should_return_false_if_file_with_tabs_is_found(self):
        self.given_a_file_in_test_dir('invalid.js', INVALID_JS)
        self.assertFalse(DebugStatements(self.options).run())

    def test_analysis_should_return_true_if_file_with_tabs_is_excluded(self):
        filename = 'invalid.js'
        self.given_a_file_in_test_dir(filename, INVALID_JS)
        self.options['debug-statements-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(DebugStatements(self.options).run())

    def test_analysis_should_return_true_for_non_watched_file_with_tabs(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_JS)
        self.assertTrue(DebugStatements(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.js', INVALID_JS)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
