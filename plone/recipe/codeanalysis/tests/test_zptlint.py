# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.zptlint import ZPTLint
from shutil import rmtree
from tempfile import mkdtemp

import os
import unittest

# EXTRAS_INSTALLED is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
ZPTLINT_INSTALLED = os.environ.get('EXTRAS_INSTALLED', False)

VALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p tal:content="string:Hello World!" />
  </body>
</html>
"""

INVALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p tal:content="python:Hello World!" />
  </body>
</html>
"""


class ZPTLintTestCase(unittest.TestCase):

    def setUp(self):  # noqa
        self.options = {
            'zptlint': 'True',
            'zptlint-bin': 'bin/zptlint',
        }
        if os.path.isfile('../../bin/zptlint'):  # when cwd is parts/test
            self.options['zptlint-bin'] = '../../bin/zptlint'
        self.test_dir = mkdtemp()

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        with open(os.path.join(self.test_dir, 'invalid.pt'), 'w') as f:
            f.write(INVALID_CODE)
        self.options['directory'] = self.test_dir
        self.assertFalse(ZPTLint(self.options).run())

    def test_analysis_should_return_false_when_oserror(self):
        with open(os.path.join(self.test_dir, 'invalid.pt'), 'w') as f:
            f.write(INVALID_CODE)
        self.options['zptlint-bin'] = ''
        self.options['directory'] = self.test_dir
        self.assertFalse(ZPTLint(self.options).run())

    @unittest.skipIf(not ZPTLINT_INSTALLED, 'zptlint is not installed')
    def test_analysis_should_return_true(self):
        with open(os.path.join(self.test_dir, 'valid.pt'), 'w') as f:
            f.write(VALID_CODE)
        self.options['directory'] = self.test_dir
        self.assertTrue(ZPTLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        with open(os.path.join(self.test_dir, 'valid.pt'), 'w') as f:
            f.write(VALID_CODE)
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        ZPTLint(self.options).run()
        file_exists = os.path.isfile(
            os.path.join(location_tmp_dir, 'zptlint.log'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exists)
