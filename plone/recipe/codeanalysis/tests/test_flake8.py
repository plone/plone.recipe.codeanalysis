# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from plone.recipe.codeanalysis.flake8 import Flake8
from plone.recipe.codeanalysis.flake8 import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
import os

VALID_CODE = '''\
# -*- coding: utf-8 -*-
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
        # flake8-quotes could not handle this
        # return "hello world"  # noqa
'''

INVALID_CODE = '''\
# -*- coding: utf-8 -*-
def foo(bar):
    """
    A docstring with a "comment"
    """
    if ('foo' == "bar"):
        return 'foobar'
'''

SINGLE_IN_DOUBLE = '''\
# -*- coding: utf-8 -*-
print("this is a string with 'quotes'.")
'''

DOUBLE_IN_SINGLE = """\
# -*- coding: utf-8 -*-
print('this is a string with "quotes".')
"""

# flake8-debugger
PDB_STATEMENT = """\
# -*- coding: utf-8 -*-
import pdb; pdb.set_trace()
"""

IPDB_STATEMENT = """\
# -*- coding: utf-8 -*-
import pdb; pdb.set_trace()
"""

# pep8-naming
INVALID_NAMING_STATEMENT = """\
# -*- coding: utf-8 -*-
def Foo(bar):
    return bar
"""

# flake8-blind-except
INVALID_EXCEPT = """\
# -*- coding: utf-8 -*-
try:
    assert False
except:
    assert False
"""  # noqa

VALID_EXCEPT = """\
# -*- coding: utf-8 -*-
try:
    assert False
except Exception:
    assert False
"""

# missing utf8 header
MISSING_CODING = """\
def foo(bar)
    return bar
"""


class TestFlake8(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestFlake8, self).setUp()
        self.options.update({
            'flake8-ignore': '',
            'flake8-exclude': 'bootstrap.py,bootstrap-buildout.py,docs,*.egg',
            'flake8-max-complexity': '10',
            'flake8-max-line-length': '79',
        })
        if os.path.isfile('../../bin/flake8'):  # when cwd is parts/test
            self.options['bin-directory'] = '../../bin'

    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('incorrect.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'import sys',
            'class MyClass():',
            '    def __init__(self):',
            '        my_sum=1+1'  # No space between operators.
            '',
        ]))
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['bin-directory'] = 'FAKE_DIR'
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('correct.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'class MyClass():',
            '    def __init__(self):',
            '        my_sum = 1 + 1',
            '        self.my_sum = my_sum',
            '',
        ]))
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        parts_dir = mkdtemp()
        self.given_a_file_in_test_dir('correct.py', '\n'.join([
            'class MyClass():',
            '    def __init__(self):',
            '        my_sum = 1 + 1',
            '        self.my_sum = my_sum',
            '',
        ]))
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        Flake8(self.options).run()
        file_exist = os.path.isfile(os.path.join(parts_dir, 'flake8.log'))
        rmtree(parts_dir)
        self.assertTrue(file_exist)

    def test_analysis_should_return_false_if_double_quotes_found(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self.given_a_file_in_test_dir(filename, INVALID_CODE)
        self.options['flake8-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_true_for_valid_files(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_true_if_double_in_single_quotes(self):
        self.given_a_file_in_test_dir('double_in_single.py', DOUBLE_IN_SINGLE)
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_false_if_single_in_double_quotes(self):
        self.given_a_file_in_test_dir('single_in_double.py', SINGLE_IN_DOUBLE)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_if_pdb_found(self):
        self.given_a_file_in_test_dir('pdb.py', PDB_STATEMENT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_if_ipdb_found(self):
        self.given_a_file_in_test_dir('ipdb.py', IPDB_STATEMENT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_on_invalid_method_naming(self):
        self.given_a_file_in_test_dir('naming.py', INVALID_NAMING_STATEMENT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_on_invalid_except_statement(self):
        self.given_a_file_in_test_dir('invalid_except.py', INVALID_EXCEPT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_true_on_valid_except_statement(self):
        self.given_a_file_in_test_dir('valid_except.py', VALID_EXCEPT)
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_false_if_coding_missing(self):
        self.given_a_file_in_test_dir('missing_coding.py', MISSING_CODING)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
