# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from plone.recipe.codeanalysis.flake8 import console_script
from plone.recipe.codeanalysis.flake8 import Flake8
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os


INVALID_CODE = '''\
# -*- coding: utf-8 -*-
def foo(bar):
    """
    A docstring with a "comment"
    """
    if ('foo' == "bar"):
        return 'foobar'
'''

VALID_CODE = """
# -*- coding: utf-8 -*-


class MyClass():
    def __init__(self):
        my_sum = 1 + 1
        self.my_sum = my_sum
"""

ISORT_CFG = """
[settings]
force_alphabetical_sort = True
force_single_line = True
lines_after_imports = 2
line_length = 200
not_skip = __init__.py
"""


class TestFlake8(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestFlake8, self).setUp()
        self.flake8_default_options = {
            'flake8-ignore': '',
            'flake8-exclude': 'bootstrap.py,bootstrap-buildout.py,docs,*.egg',
            'flake8-max-complexity': '10',
            'flake8-max-line-length': '79',
        }
        self.options.update(self.flake8_default_options)
        if os.path.isfile('../../bin/flake8'):  # when cwd is parts/test
            self.options['bin-directory'] = '../../bin'
        self.given_a_file_in_test_dir('.isort.cfg', ISORT_CFG)

    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('incorrect.py', INVALID_CODE)
        with OutputCapture():
            self.assertFalse(Flake8(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['bin-directory'] = 'FAKE_DIR'
        with OutputCapture():
            self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('correct.py', VALID_CODE)
        with OutputCapture():
            self.assertTrue(Flake8(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        parts_dir = mkdtemp()
        self.given_a_file_in_test_dir('correct.py', VALID_CODE)
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            Flake8(self.options).run()
        file_exist = os.path.isfile(os.path.join(parts_dir, 'flake8.log'))
        rmtree(parts_dir)
        self.assertTrue(file_exist)

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self.given_a_file_in_test_dir(filename, INVALID_CODE)
        self.options['flake8-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename,
        )
        with OutputCapture():
            self.assertTrue(Flake8(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)

    def test_get_flake8_options(self):
        self.options.update({
            'flake8-one': 'something',
            'flake8-two': 'else',
        })
        options = Flake8(self.options).get_flake8_options()
        self.assertEqual(
            len(options),
            # --one=something --two=else --jobs=1 + default options
            2 + 1 + len(self.flake8_default_options),
        )

    def test_get_flake8_options_ignored(self):
        self.options.update({
            'flake8-one': 'something',
            'flake8-filesystem': 'ignored',
            'flake8-extensions': 'ignored',
        })
        options = Flake8(self.options).get_flake8_options()
        self.assertEqual(
            len(options),
            # --one=something --jobs=1 + default options
            1 + 1 + len(self.flake8_default_options),
        )

    def test_get_flake8_options_on_deactivated_multiprocessing(self):
        self.options.update({
            'multiprocessing': 'True',
        })
        options = Flake8(self.options).get_flake8_options()
        self.assertEqual(
            len(options),
            len(self.flake8_default_options),  # just default options
        )
