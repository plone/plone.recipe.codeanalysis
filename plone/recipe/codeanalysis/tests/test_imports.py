# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.isort import console_script
from plone.recipe.codeanalysis.isort import Isort
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from testfixtures import OutputCapture

import os


VALID = '\n'.join([
    'from Foo.bar import baz',
    'from foo.Bar import baz',
    'from foo.bar import Baz',
    'from foo.bar import baz',
    '',
    'import baz',
])

VALID_MULTILINE = '\n'.join([
    'from foo.bar import baz',
    'from foo.bar import \\',
    '    this_is_a_very_long_baz_which_for_sure_exceeds_line_length',
    '',
    'import baz',
])

VALID_MULTIPLE_MULTILINE = '\n'.join([
    'from foo.bar import baz',
    'from foo.bar import \\',
    '    this_is_a_very_long_baz_which_for_sure_exceeds_line_length',
    'from foo.car import \\',
    '    this_is_a_very_long_baz_which_for_sure_exceeds_line_length',
    '',
    'import baz',
])

VALID_IGNORED_SORTED = '\n'.join([
    'from Foo.bar import Baz',
    'from Foo.bar import baz  # noqa',
    'from foo.Bar import baz',
    'from foo.bar import baz',
    '',
    'import baz',
    'import Baz  # noqa',
])

INVALID_SORTED = '\n'.join([
    'from Foo.bar import baz',
    'from foo.bar import Baz',
    'from foo.Bar import baz',
    'from foo.bar import baz',
    '',
    'import baz',
])

INVALID_MULTILINE = '\n'.join([
    'from foo.bar import \\',
    '    this_is_a_very_long_baz',
    'from foo.bar import baz',
    '',
    'import baz',
])

INVALID_MULTIPLE_MULTILINE = '\n'.join([
    'from foo.bar import \\',
    '    this_is_a_very_long_baz',
    'from foo.bar import z_baz',
    'from foo.bar import \\',
    '    this_is_another_very_long_baz',
    '',
    'import baz',
])

INVALID_MISSING_NL = '\n'.join([
    'from foo.bar import bar',
    'from foo.bar import baz',
    'import baz',
])

INVALID_GROUPED = '\n'.join([
    'from Foo import (bar, baz)',
    'from foo import Baz, baz',
])

INVALID_RELATIVE = '\n'.join([
    'from . import Foo'
])

INVALID_RELATIVE_PARENT = '\n'.join([
    'from .. import Bar'
])


class TestIsort(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestIsort, self).setUp()
        self.options.update({
            'isort': 'True',
            'isort-diff': 'False',
            'isort-exclude': '',
        })
        if os.path.isfile('../../bin/isort'):  # when cwd is parts/test
            self.options['bin-directory'] = '../../bin'

    def test_analysis_should_return_true_for_no_files(self):
        with OutputCapture():
            self.assertTrue(Isort(self.options).run())

    def test_analysis_should_return_true_for_valid_imports(self):
        self.given_a_file_in_test_dir('valid.py', VALID)
        with OutputCapture():
            self.assertTrue(Isort(self.options).run())

    def test_analysis_should_return_true_for_valid_multi_imports(self):
        self.given_a_file_in_test_dir('valid.py', VALID_MULTILINE)
        with OutputCapture():
            self.assertTrue(Isort(self.options).run())

    def test_analysis_should_return_true_for_2_valid_multi_imports(self):
        self.given_a_file_in_test_dir('valid.py', VALID_MULTIPLE_MULTILINE)
        with OutputCapture():
            self.assertTrue(Isort(self.options).run())

    def test_analysis_should_return_true_for_unsorted_ignored_imports(self):
        self.given_a_file_in_test_dir('valid.py', VALID_IGNORED_SORTED)
        with OutputCapture():
            self.assertTrue(Isort(self.options).run())

    def test_analysis_should_return_false_on_grouped_imports(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_GROUPED)
        with OutputCapture():
            self.assertFalse(Isort(self.options).run())

    def test_analysis_should_return_false_on_unsorted_imports(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_SORTED)
        with OutputCapture():
            self.assertFalse(Isort(self.options).run())

    def test_analysis_should_return_false_on_unsorted_multi_imports(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_MULTILINE)
        with OutputCapture():
            self.assertFalse(Isort(self.options).run())

    def test_analysis_should_return_false_on_missing_newline(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_MISSING_NL)
        with OutputCapture():
            self.assertFalse(Isort(self.options).run())

    def test_analysis_should_return_false_on_2_unsorted_multi_imports(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_MULTIPLE_MULTILINE)
        with OutputCapture():
            self.assertFalse(Isort(self.options).run())

    def test_analysis_should_return_false_on_relative_import(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_RELATIVE)
        with OutputCapture():
            self.assertFalse(Isort(self.options).run())

    def test_analysis_should_return_true_on_invalid_but_ignored(self):
        filename = 'invalid.py'
        self.given_a_file_in_test_dir(filename, INVALID_RELATIVE)
        self.options['imports-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        with OutputCapture():
            self.assertTrue(Isort(self.options).run())

    def test_analysis_should_return_false_on_relative_parent_import(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_RELATIVE_PARENT)
        with OutputCapture():
            self.assertFalse(Isort(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_GROUPED)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
