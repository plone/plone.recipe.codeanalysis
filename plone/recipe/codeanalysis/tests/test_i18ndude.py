# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.i18ndude import I18NDude
from plone.recipe.codeanalysis.i18ndude import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
import os
import unittest

# EXTRAS_INSTALLED is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
I18NDUDE_INSTALLED = os.environ.get('EXTRAS_INSTALLED', False)
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
        self.options.update({
            'find-untranslated': 'True',
            'i18ndude-bin': 'bin/i18ndude',
        })
        if os.path.isfile('../../bin/i18ndude'):  # when cwd is parts/test
            self.options['i18ndude-bin'] = '../../bin/i18ndude'

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        self.assertFalse(I18NDude(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['i18ndude-bin'] = ''
        self.assertTrue(I18NDude(self.options).run())

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        self.assertTrue(I18NDude(self.options).run())

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true_if_file_invalid_is_excluded(self):
        filename = 'invalid.pt'
        self.given_a_file_in_test_dir(filename, INVALID_CODE)
        self.options['find-untranslated-exclude'] = '{0:s}/{1:s}'.format(
            self.test_dir, filename
        )
        self.assertTrue(I18NDude(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    @unittest.skipIf(not I18NDUDE_INSTALLED, I18NDUDE_NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
