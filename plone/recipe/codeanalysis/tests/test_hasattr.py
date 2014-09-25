# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis import py_hasattr
from shutil import rmtree
from tempfile import mkdtemp
import os
import unittest


VALID = [
    'def fib(n):',
    '    if n == 0: return 0',
    '    elif n == 1: return 1',
    '    else: return F(n - 1) + F(n - 2)',
    'some_my_hasattr(x)'
    'if True:'
    '    some_my_hasattr(x)'
]

VALID_IGNORE = [
    'def fib(n):',
    '    if n == 0: return 0',
    '    hasattr(n, "fib")  # noqa',  # noqa
    '    hasattr(n, "fib")  #noqa',  # noqa
    '    hasattr(n, "fib")  #  noqa',  # noqa
    '    hasattr(n, "fib")  # noqa because its fine',
    '    elif n == 1: return 1',
    '    else: return F(n - 1) + F(n - 2)',
    'hasattr(n, "fib")  # noqa',  # noqa
]

INVALID_NO_IGNORE = [
    'def fib(n):',
    '    if n == 0: return 0',
    '    hasattr(n, "fib")',  # noqa
    '    hasattr(n, "fib") # some comment',  # noqa
    '    elif n == 1: return 1',
    '    else: return F(n - 1) + F(n - 2)',
    'hasattr(n, "fib")',  # noqa
    'hasattr(n, "fib") # some comment',  # noqa
    'if hasattr(n, "fib"):',  # noqa
]


class TestHasattr(unittest.TestCase):

    def setUp(self):
        self.options = {
            'hasattr': 'True',
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
        self.assertTrue(py_hasattr.code_analysis_hasattr(self.options))

    def test_analysis_should_return_true_if_there_is_no_hasattr(self):
        self._create_file_in_test_dir('valid.py', VALID)
        self.assertTrue(py_hasattr.code_analysis_hasattr(self.options))

    def test_analysis_should_return_true_if_there_noqa(self):
        self._create_file_in_test_dir('valid.py', VALID_IGNORE)
        self.assertTrue(py_hasattr.code_analysis_hasattr(self.options))

    def test_analysis_should_return_errors_if_there_is_hasattr(self):
        self.assertEqual(
            len(
                py_hasattr._code_analysis_hasattr_lines_parser(
                    INVALID_NO_IGNORE,
                    'invalid.py'
                )
            ),
            5
        )

    def test_analysis_should_return_false_if_there_is_hasattr(self):
        self._create_file_in_test_dir('invalid.py', INVALID_NO_IGNORE)
        self.assertFalse(py_hasattr.code_analysis_hasattr(self.options))
