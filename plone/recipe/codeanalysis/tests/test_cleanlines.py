# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.clean_lines import code_analysis_clean_lines
from shutil import rmtree
from tempfile import mkdtemp
import os
import unittest

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


class TestCleanLines(unittest.TestCase):

    def setUp(self):
        self.options = {
            'clean-lines': 'True',
            'clean-lines-exclude': '',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def _create_file_in_test_dir(self, filename, contents):
        with open(os.path.join(self.test_dir, filename), 'w') as f:
            f.write(contents)
        self.options['directory'] = self.test_dir

    def test_analysis_should_return_false_if_trailing_spaces_are_found(self):
        self._create_file_in_test_dir('invalid.py', INVALID_CODE)
        self.assertFalse(code_analysis_clean_lines(self.options))

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self._create_file_in_test_dir(filename, INVALID_CODE)
        self.options['clean-lines-exclude'] = \
            '{0:s}/{1:s}'.format(self.test_dir, filename)

        self.assertTrue(code_analysis_clean_lines(self.options))

    def test_analysis_should_return_true_for_valid_files(self):
        self._create_file_in_test_dir('valid.py', VALID_CODE)
        self.assertTrue(code_analysis_clean_lines(self.options))

    def test_analysis_should_return_false_if_file_with_tabs_is_found(self):
        self._create_file_in_test_dir('invalid.xml', INVALID_TABS)
        self.assertFalse(code_analysis_clean_lines(self.options))

    def test_analysis_should_return_true_if_file_with_tabs_is_excluded(self):
        filename = 'invalid.xml'
        self._create_file_in_test_dir(filename, INVALID_TABS)
        self.options['clean-lines-exclude'] = \
            '{0:s}/{1:s}'.format(self.test_dir, filename)

        self.assertTrue(code_analysis_clean_lines(self.options))

    def test_analysis_should_return_true_for_non_watched_file_with_tabs(self):
        filename = 'invalid.abc'
        self._create_file_in_test_dir(filename, INVALID_TABS)
        self.assertTrue(code_analysis_clean_lines(self.options))

    def test_analysis_should_return_true_for_non_watched_file_with_ts(self):
        filename = 'invalid.abc'
        self._create_file_in_test_dir(filename, INVALID_CODE)
        self.assertTrue(code_analysis_clean_lines(self.options))
