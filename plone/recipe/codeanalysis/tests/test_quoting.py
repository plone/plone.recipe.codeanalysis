# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.quoting import PreferSingleQuotes
from shutil import rmtree
from tempfile import mkdtemp
import os
import unittest

VALID_CODE = '''\
def foobar():
    """
    A docstring with a "comment"
    """
    if ('foo' == 'bar'):
        return 'foobar'

    # A comment with "quote"
    def bar(baz):
        """a method "called" bar"""
        return baz  # could also be "baz"

    def foo(baz):
        \'\'\'a method "called" foobar\'\'\'
        return baz  # could also be 'baz'

    def foobar():
        """A complex docstring:
           Show an "example" of nested multiline \'\'\'inline string\'\'\'
           and multiline \'\'\'
           multiline string with again a containing "quote"
           \'\'\'
           here we are.  # and 'nowhere' "else"
        """
        return "hello world"  # noqa
'''

INVALID_CODE = '''\
    def foo(bar):
        """
        A docstring with a "comment"
        """
        if ('foo' == "bar"):
            return 'foobar'
'''

SINGLE_IN_DOUBLE = '''print "this is a string with 'quotes'."'''
DOUBLE_IN_SINGLE = """print 'this is a string with "quotes".'"""


class TestCleanLines(unittest.TestCase):

    def setUp(self):
        self.options = {
            'prefer-single-quotes': 'True',
            'prefer-single-quotes-exclude': '',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def _create_file_in_test_dir(self, filename, contents):
        with open(os.path.join(self.test_dir, filename), 'w') as f:
            f.write(contents)
        self.options['directory'] = self.test_dir

    def test_analysis_should_return_false_if_double_quotes_found(self):
        self._create_file_in_test_dir('invalid.py', INVALID_CODE)
        self.assertFalse(PreferSingleQuotes(self.options).run())

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self._create_file_in_test_dir(filename, INVALID_CODE)
        self.options['prefer-single-quotes-exclude'] = \
            '{0:s}/{1:s}'.format(self.test_dir, filename)

        self.assertTrue(PreferSingleQuotes(self.options).run())

    def test_analysis_should_return_true_for_valid_files(self):
        self._create_file_in_test_dir('valid.py', VALID_CODE)
        self.assertTrue(PreferSingleQuotes(self.options).run())

    def test_analysis_should_return_true_if_double_in_single_quotes(self):
        self._create_file_in_test_dir('double_in_single.py', DOUBLE_IN_SINGLE)
        self.assertTrue(PreferSingleQuotes(self.options).run())

    def test_analysis_should_return_false_if_single_in_double_quotes(self):
        self._create_file_in_test_dir('single_in_double.py', SINGLE_IN_DOUBLE)
        self.assertFalse(PreferSingleQuotes(self.options).run())
