# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.deprecated_aliases import DeprecatedAliases
from shutil import rmtree
from tempfile import mkdtemp
import os
import unittest

INVALID_CODE = """\
# -*- coding: utf-8 -*-
import unittest


class Test1(unittest.TestCase):

    def test_unless(self):
        self.assertUnless(True)

    def test_unless_equals(self):
        self.assertUnlessEqual(True, True)

    def test_unless_raises(self):
        self.failUnlessRaises(Exception, foo)

    def test_unless_equals(self):
        self.assertUnlessEqual(True, True)

    def test_fail_if(self):
        self.failIf(True)
"""

VALID_CODE = """\
# -*- coding: utf-8 -*-
import unittest


class Test2(unittest.TestCase):

    def test_fail_if(self):
        self.failIf(True)  # noqa
"""


class TestDeprecatedAliases(unittest.TestCase):

    def setUp(self):  # noqa
        self.options = {
            'deprecated-aliases': 'True',
            'deprecated-aliases-exclude': '',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def _create_file_in_test_dir(self, filename, contents):
        with open(os.path.join(self.test_dir, filename), 'w') as f:
            f.write(contents)
        self.options['directory'] = self.test_dir

    def test_analysis_should_return_false_if_deprecated_alias_found(self):
        self._create_file_in_test_dir('invalid.py', INVALID_CODE)
        self.assertFalse(DeprecatedAliases(self.options).run())

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self._create_file_in_test_dir(filename, INVALID_CODE)
        self.options['deprecated-aliases-exclude'] = \
            '{0:s}/{1:s}'.format(self.test_dir, filename)
        self.assertTrue(DeprecatedAliases(self.options).run())

    def test_analysis_should_return_true_for_valid_files(self):
        self._create_file_in_test_dir('valid.py', VALID_CODE)
        self.assertTrue(DeprecatedAliases(self.options).run())
