# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.clean_lines import CleanLines
from plone.recipe.codeanalysis.clean_lines import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase

VALID_CODE = """\
def foo(bar):
    return 'foo'
"""

INVALID_CODE = """\
def foo(bar):
    return 'foo' \

"""

INVALID_TABS = """\
<a>
\t<b>foo</b>
</a>"""


class TestCleanLines(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestCleanLines, self).setUp()
        self.options.update({
            'clean-lines': 'True',
            'clean-lines-exclude': '',
        })

    def test_analysis_should_return_false_if_trailing_spaces_are_found(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        self.assertFalse(CleanLines(self.options).run())

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self.given_a_file_in_test_dir(filename, INVALID_CODE)
        self.options['clean-lines-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(CleanLines(self.options).run())

    def test_analysis_should_return_true_for_valid_files(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        self.assertTrue(CleanLines(self.options).run())

    def test_analysis_should_return_false_if_file_with_tabs_is_found(self):
        self.given_a_file_in_test_dir('invalid.xml', INVALID_TABS)
        self.assertFalse(CleanLines(self.options).run())

    def test_analysis_should_return_true_if_file_with_tabs_is_excluded(self):
        filename = 'invalid.xml'
        self.given_a_file_in_test_dir(filename, INVALID_TABS)
        self.options['clean-lines-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(CleanLines(self.options).run())

    def test_analysis_should_return_true_for_non_watched_file_with_tabs(self):
        self.given_a_file_in_test_dir('invalid.abc', INVALID_TABS)
        self.assertTrue(CleanLines(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_TABS)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
