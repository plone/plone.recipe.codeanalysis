# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.imports import code_analysis_imports
from shutil import rmtree
from tempfile import mkdtemp
import os
import unittest

VALID = [
    'from Foo.bar import baz',
    'from foo.Bar import baz',
    'from foo.bar import Baz',
    'from foo.bar import baz',
    'import baz',
]

VALID_MULTILINE = [
    'from foo.bar import baz',
    'from foo.bar import \\',
    '    this_is_a_very_long_baz',
    'import baz',
]

VALID_MULTIPLE_MULTILINE = [
    'from foo.bar import baz',
    'from foo.bar import \\',
    '    this_is_a_very_long_baz',
    'from foo.car import \\',
    '    this_is_a_very_long_baz',
    'import baz',
]

VALID_IGNORED_SORTED = [
    'from Foo.bar import Baz',
    'from Foo.bar import baz  # noqa',
    'from foo.Bar import baz',
    'from foo.bar import baz',
    'import baz',
    'import Baz  # noqa',
]

INVALID_SORTED = [
    'from Foo.bar import baz',
    'from foo.bar import Baz',
    'from foo.Bar import baz',
    'from foo.bar import baz',
    'import baz',
]

INVALID_MULTILINE = [
    'from foo.bar import \\',
    '    this_is_a_very_long_baz',
    'from foo.bar import baz',
    'import baz',
]

INVALID_MULTIPLE_MULTILINE = [
    'from foo.bar import \\',
    '    this_is_a_very_long_baz',
    'from foo.bar import z_baz',
    'from foo.bar import \\',
    '    this_is_another_very_long_baz',
    'import baz',
]

INVALID_GROUPED = [
    'from Foo import (bar, baz)',
    'from foo import Baz, baz',
]


class TestImports(unittest.TestCase):

    def setUp(self):
        self.options = {
            'imports': 'True',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def _create_file_in_test_dir(self, filename, contents):
        with open(os.path.join(self.test_dir, filename), 'w') as f:
            f.write('\n'.join(contents))
        self.options['directory'] = self.test_dir

    def test_analysis_should_return_true_for_no_files(self):
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_imports(self.options))

    def test_analysis_should_return_true_for_valid_imports(self):
        self._create_file_in_test_dir('valid.py', VALID)
        self.assertTrue(code_analysis_imports(self.options))

    def test_analysis_should_return_true_for_valid_multi_imports(self):
        self._create_file_in_test_dir('valid.py', VALID_MULTILINE)
        self.assertTrue(code_analysis_imports(self.options))

    def test_analysis_should_return_true_for_2_valid_multi_imports(self):
        self._create_file_in_test_dir('valid.py', VALID_MULTIPLE_MULTILINE)
        self.assertTrue(code_analysis_imports(self.options))

    def test_analysis_should_return_true_for_unsorted_ignored_imports(self):
        self._create_file_in_test_dir('valid.py', VALID_IGNORED_SORTED)
        self.assertTrue(code_analysis_imports(self.options))

    def test_analysis_should_return_false_on_grouped_imports(self):
        self._create_file_in_test_dir('invalid.py', INVALID_GROUPED)
        self.assertFalse(code_analysis_imports(self.options))

    def test_analysis_should_return_false_on_unsorted_imports(self):
        self._create_file_in_test_dir('invalid.py', INVALID_SORTED)
        self.assertFalse(code_analysis_imports(self.options))

    def test_analysis_should_return_false_on_unsorted_multi_imports(self):
        self._create_file_in_test_dir('invalid.py', INVALID_MULTILINE)
        self.assertFalse(code_analysis_imports(self.options))

    def test_analysis_should_return_false_on_2_unsorted_multi_imports(self):
        self._create_file_in_test_dir('invalid.py', INVALID_MULTIPLE_MULTILINE)
        self.assertFalse(code_analysis_imports(self.options))
