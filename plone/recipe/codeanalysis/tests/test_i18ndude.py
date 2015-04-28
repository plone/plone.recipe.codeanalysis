# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.i18ndude import I18NDude
from shutil import rmtree
from tempfile import mkdtemp

import os
import unittest

# EXTRAS_INSTALLED is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
I18NDUDE_INSTALLED = os.environ.get('EXTRAS_INSTALLED', False)

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


class I18NDudeTestCase(unittest.TestCase):

    def setUp(self):  # noqa
        self.options = {
            'find-untranslated': 'True',
            'i18ndude-bin': 'bin/i18ndude',
        }
        if os.path.isfile('../../bin/i18ndude'):  # when cwd is parts/test
            self.options['i18ndude-bin'] = '../../bin/i18ndude'
        self.test_dir = mkdtemp()

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        with open(os.path.join(self.test_dir, 'invalid.pt'), 'w') as f:
            f.write(INVALID_CODE)
        self.options['directory'] = self.test_dir
        self.assertFalse(I18NDude(self.options).run())

    def test_analysis_should_return_false_when_oserror(self):
        with open(os.path.join(self.test_dir, 'invalid.pt'), 'w') as f:
            f.write(INVALID_CODE)
        self.options['i18ndude-bin'] = ''
        self.options['directory'] = self.test_dir
        self.assertFalse(I18NDude(self.options).run())

    # this test should run only if i18ndude is installed
    @unittest.skipIf(not I18NDUDE_INSTALLED, 'i18ndude is not installed')
    def test_analysis_should_return_true(self):
        with open(os.path.join(self.test_dir, 'valid.pt'), 'w') as f:
            f.write(VALID_CODE)
        self.options['directory'] = self.test_dir
        self.assertTrue(I18NDude(self.options).run())
