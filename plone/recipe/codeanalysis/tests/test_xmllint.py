# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from plone.recipe.codeanalysis.xmllint import console_script
from plone.recipe.codeanalysis.xmllint import XMLLint
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os
import unittest


# EXTRAS_INSTALLED is an environment variable that we set on
# Travis CI to indicate all external dependencies are, in fact,
# installed; we used it as a flag to skip some tests here
XMLLINT_INSTALLED = os.environ.get('EXTRAS_INSTALLED', False)
XMLLINT_NOT_INSTALLED_MSG = 'xmllint is not installed'

VALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p>Hello World!</p>
  </body>
</html>
"""

INVALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p>Hello <em>World!</p></em>
  </body>
</html>
"""


class TestXMLLint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestXMLLint, self).setUp()
        self.options.update({
            'xmllint': 'True',
            'xmllint-bin': 'bin/xmllint',
        })
        if os.path.isfile('../../bin/xmllint'):  # when cwd is parts/test
            self.options['xmllint-bin'] = '../../bin/xmllint'

    @unittest.skipIf(not XMLLINT_INSTALLED, XMLLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('invalid.xml', INVALID_CODE)
        with OutputCapture():
            self.assertFalse(XMLLint(self.options).run())

    @unittest.skipIf(not XMLLINT_INSTALLED, XMLLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('valid.xml', VALID_CODE)
        with OutputCapture():
            self.assertTrue(XMLLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        self.given_a_file_in_test_dir('valid.xml', VALID_CODE)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            XMLLint(self.options).run()
        file_exists = os.path.isfile(os.path.join(parts_dir, 'xmllint.log'))
        rmtree(parts_dir)
        self.assertTrue(file_exists)

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.xml', VALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    @unittest.skipIf(not XMLLINT_INSTALLED, XMLLINT_NOT_INSTALLED_MSG)
    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.xml', INVALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
