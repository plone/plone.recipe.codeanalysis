# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.i18ndude import code_analysis_find_untranslated
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


class i18ndudeTestCase(unittest.TestCase):
    def setUp(self):
        self.options = {
            'find-untranslated': 'True',
            'i18ndude-bin': 'bin/i18ndude',
        }
        if os.path.isfile('../../bin/i18ndude'):  # when cwd is parts/test
            self.options['i18ndude-bin'] = '../../bin/i18ndude'
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        with open(os.path.join(self.test_dir, 'invalid.pt'), 'w') as f:
            f.write(INVALID_CODE)
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_find_untranslated(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        with open(os.path.join(self.test_dir, 'invalid.pt'), 'w') as f:
            f.write(INVALID_CODE)
        self.options['i18ndude-bin'] = ''
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_find_untranslated(self.options))

    # this test should run only if i18ndude is installed
    @unittest.skipIf(not I18NDUDE_INSTALLED, 'i18ndude is not installed')
    def test_analysis_should_return_true(self):
        with open(os.path.join(self.test_dir, 'valid.pt'), 'w') as f:
            f.write(VALID_CODE)
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_find_untranslated(self.options))

    @unittest.expectedFailure  # Jenkins support is not yet implemented
    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        with open(os.path.join(self.test_dir, 'valid.pt'), 'w') as f:
            f.write(VALID_CODE)
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_find_untranslated(self.options)
        file_exists = os.path.isfile(
            os.path.join(location_tmp_dir, 'i18ndude.log'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exists)
