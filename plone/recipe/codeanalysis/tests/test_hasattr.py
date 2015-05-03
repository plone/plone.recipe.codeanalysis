# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.py_hasattr import HasAttr
from plone.recipe.codeanalysis.py_hasattr import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase

VALID = '\n'.join([
    'def fib(n):',
    '    if n == 0: return 0',
    '    elif n == 1: return 1',
    '    else: return F(n - 1) + F(n - 2)',
    'some_my_hasattr(x)'
    'if True:'
    '    some_my_hasattr(x)'
])

VALID_IGNORE = '\n'.join([
    'def fib(n):',
    '    if n == 0: return 0',
    '    hasattr(n, "fib")  # noqa',  # noqa
    '    hasattr(n, "fib")  # noqa because its fine',
    '    elif n == 1: return 1',
    '    else: return F(n - 1) + F(n - 2)',
    'hasattr(n, "fib")  # noqa',  # noqa
])

INVALID_NO_IGNORE = '\n'.join([
    'def fib(n):',
    '    if n == 0: return 0',
    '    hasattr(n, "fib")',  # noqa
    '    hasattr(n, "fib") # some comment',  # noqa
    '    elif n == 1: return 1',
    '    else: return F(n - 1) + F(n - 2)',
    'hasattr(n, "fib")',  # noqa
    'hasattr(n, "fib") # some comment',  # noqa
    'if hasattr(n, "fib"):',  # noqa
])


class TestHasattr(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestHasattr, self).setUp()
        self.options.update({
            'hasattr': 'True',
        })

    def test_analysis_should_return_true_for_no_files(self):
        self.assertTrue(HasAttr(self.options).run())

    def test_analysis_should_return_true_if_there_is_no_hasattr(self):
        self.given_a_file_in_test_dir('valid.py', VALID)
        self.assertTrue(HasAttr(self.options).run())

    def test_analysis_should_return_true_if_there_noqa(self):
        self.given_a_file_in_test_dir('valid.py', VALID_IGNORE)
        self.assertTrue(HasAttr(self.options).run())

    def test_analysis_should_return_false_if_there_is_hasattr(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_NO_IGNORE)
        self.assertFalse(HasAttr(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.py', VALID)
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_NO_IGNORE)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
