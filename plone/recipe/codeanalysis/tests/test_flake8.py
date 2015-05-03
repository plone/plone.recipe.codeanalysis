# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import open
from os.path import isfile as path_isfile
from os.path import join as path_join
from plone.recipe.codeanalysis.flake8 import Flake8
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase

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


class TestFlake8(TestCase):

    def setUp(self):  # noqa
        self.test_dir = mkdtemp()
        self.options = {
            'bin-directory': 'bin/',
            'flake8-ignore': '',
            'flake8-exclude': 'bootstrap.py,bootstrap-buildout.py,docs,*.egg',
            'flake8-max-complexity': '10',
            'flake8-max-line-length': '79',
            'jenkins': 'False',
            'directory': self.test_dir,
        }
        if path_isfile('../../bin/flake8'):  # when cwd is parts/test
            self.options['bin-directory'] = '../../bin'

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        with open(path_join(self.test_dir, 'incorrect.py'), 'w') as f:
            f.write(
                '# -*- coding: utf-8 -*-\n'
                'import sys\n'
                'class MyClass():\n'
                '    def __init__(self):\n'
                '        my_sum=1+1')  # No space between operators.
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['bin-directory'] = 'FAKE_DIR'
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_true(self):
        with open(path_join(self.test_dir, 'incorrect.py'), 'w') as f:
            f.write(
                '# -*- coding: utf-8 -*-\n'
                'class MyClass():\n'
                '    def __init__(self):\n'
                '        my_sum = 1 + 1\n'
                '        self.my_sum = my_sum\n')
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        with open(path_join(self.test_dir, 'correct.py'), 'w') as f:
            f.write(
                'class MyClass():\n'
                '    def __init__(self):\n'
                '        my_sum = 1 + 1\n'
                '        self.my_sum = my_sum\n')
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        Flake8(self.options).run()
        file_exist = path_isfile(path_join(location_tmp_dir, 'flake8.log'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_analysis_should_return_false_if_double_quotes_found(self):
        with open(path_join(self.test_dir, 'invalid.py'), 'w') as f:
            f.write(INVALID_CODE)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        with open(path_join(self.test_dir, filename), 'w') as f:
            f.write(INVALID_CODE)
        self.options['flake8-exclude'] = \
            '{0:s}/{1:s}'.format(self.test_dir, filename)
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_true_for_valid_files(self):
        with open(path_join(self.test_dir, 'valid.py'), 'w') as f:
            f.write(VALID_CODE)
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_true_if_double_in_single_quotes(self):
        with open(path_join(self.test_dir, 'double_in_single.py'), 'w') as f:
            f.write(DOUBLE_IN_SINGLE)
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_false_if_single_in_double_quotes(self):
        with open(path_join(self.test_dir, 'single_in_double.py'), 'w') as f:
            f.write(SINGLE_IN_DOUBLE)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_if_pdb_found(self):
        with open(path_join(self.test_dir, 'pdb.py'), 'w') as f:
            f.write(PDB_STATEMENT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_if_ipdb_found(self):
        with open(path_join(self.test_dir, 'ipdb.py'), 'w') as f:
            f.write(IPDB_STATEMENT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_on_invalid_method_naming(self):
        with open(path_join(self.test_dir, 'naming.py'), 'w') as f:
            f.write(INVALID_NAMING_STATEMENT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_false_on_invalid_except_statement(self):
        with open(path_join(self.test_dir, 'invalid_except.py'), 'w') as f:
            f.write(INVALID_EXCEPT)
        self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_true_on_valid_except_statement(self):
        with open(path_join(self.test_dir, 'valid_except.py'), 'w') as f:
            f.write(VALID_EXCEPT)
        self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_false_if_coding_missing(self):
        with open(path_join(self.test_dir, 'missing_coding.py'), 'w') as f:
            f.write(MISSING_CODING)
        self.assertFalse(Flake8(self.options).run())
