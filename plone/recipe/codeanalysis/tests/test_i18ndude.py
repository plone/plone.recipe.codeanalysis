# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.i18ndude import console_script
from plone.recipe.codeanalysis.i18ndude import I18NDude
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from testfixtures import OutputCapture

import os
import unittest


# TEST_ALL is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
I18NDUDE_INSTALLED = os.environ.get('TEST_ALL', False)
I18NDUDE_NOT_INSTALLED_MSG = 'i18ndude is not installed'

VALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n">
  <body>
    <p i18n:translate="">Hello World!</p>
  </body>
</html>
"""

INVALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n">
  <body>
    <p>Hello World!</p>
  </body>
</html>
"""


class TestI18NDude(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestI18NDude, self).setUp()
        if os.path.isfile('../../bin/i18ndude'):  # when cwd is parts/test
            self.options['i18ndude-bin'] = '../../bin/i18ndude'

    def test_nosummary_option(self):
        i18ndude = I18NDude(self.options)
        self.assertFalse(i18ndude.nosummary)
        self.options['find-untranslated-no-summary'] = 'True'
        i18ndude = I18NDude(self.options)
        self.assertTrue(i18ndude.nosummary)

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_nosummary_cmd(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        i18ndude = I18NDude(self.options)
        self.assertNotIn('--nosummary', i18ndude.cmd)
        self.options['find-untranslated-no-summary'] = 'True'
        i18ndude = I18NDude(self.options)
        self.assertIn('--nosummary', i18ndude.cmd)

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        with OutputCapture():
            self.assertFalse(I18NDude(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['i18ndude-bin'] = ''
        with OutputCapture():
            self.assertTrue(I18NDude(self.options).run())

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        with OutputCapture():
            self.assertTrue(I18NDude(self.options).run())

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true_if_file_invalid_is_excluded(self):
        filename = 'invalid.pt'
        self.given_a_file_in_test_dir(filename, INVALID_CODE)
        self.options['find-untranslated-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename,
        )
        with OutputCapture():
            self.assertTrue(I18NDude(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
