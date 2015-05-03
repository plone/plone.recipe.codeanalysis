# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.deprecated_aliases import DeprecatedAliases
from plone.recipe.codeanalysis.deprecated_aliases import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase

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


class TestDeprecatedAliases(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestDeprecatedAliases, self).setUp()
        self.options.update({
            'deprecated-aliases': 'True',
            'deprecated-aliases-exclude': '',
        })

    def test_analysis_should_return_false_if_deprecated_alias_found(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        self.assertFalse(DeprecatedAliases(self.options).run())

    def test_analysis_should_return_true_if_invalid_file_is_excluded(self):
        filename = 'invalid.py'
        self.given_a_file_in_test_dir(filename, INVALID_CODE)
        self.options['deprecated-aliases-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(DeprecatedAliases(self.options).run())

    def test_analysis_should_return_true_for_valid_files(self):
        self.given_a_file_in_test_dir('valid.py', VALID_CODE)
        self.assertTrue(DeprecatedAliases(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.py', INVALID_CODE)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
