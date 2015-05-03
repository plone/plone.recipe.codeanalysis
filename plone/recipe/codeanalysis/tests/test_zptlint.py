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
ZPTLINT_NOT_INSTALLED_MSG = 'zptlint is not installed'

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
        self.test_dir = mkdtemp()
        self.options = {
            'zptlint': 'True',
            'zptlint-bin': 'bin/zptlint',
            'directory': self.test_dir,
        }
        if os.path.isfile('../../bin/zptlint'):  # when cwd is parts/test
            self.options['zptlint-bin'] = '../../bin/zptlint'
        # Create a valid file for each testcase
        with open(os.path.join(self.test_dir, 'valid.pt'), 'w') as f:
            f.write(VALID_CODE)

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        with open(os.path.join(self.test_dir, 'invalid.pt'), 'w') as f:
            f.write(INVALID_CODE)
        self.assertFalse(ZPTLint(self.options).run())

    def test_analysis_should_return_true_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # but return True.
        self.options['zptlint-bin'] = ''
        self.assertTrue(ZPTLint(self.options).run())

    @unittest.skipIf(not ZPTLINT_INSTALLED, ZPTLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true(self):
        self.assertTrue(ZPTLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        ZPTLint(self.options).run()
        file_exists = os.path.isfile(
            os.path.join(location_tmp_dir, 'zptlint.log'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exists)
