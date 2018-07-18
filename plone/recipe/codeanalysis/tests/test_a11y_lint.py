# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.a11y import A11yLint
from plone.recipe.codeanalysis.a11y import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os


VALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p>Hello World! -- with: &nbsp; and 2 &times; 2 = 4 --</p>
  </body>
</html>
"""

INVALID_CODE = """<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
  <body>
    <p class='">Hello World!</p>
  </body>
</html>
"""


class TestA11yLint(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestA11yLint, self).setUp()
        self.options.update({
            'a11y-lint': 'True',
        })

    def test_analysis_should_return_false_when_error_found(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        with OutputCapture():
            self.assertFalse(A11yLint(self.options).run())

    def test_analysis_should_return_true(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        with OutputCapture():
            self.assertTrue(A11yLint(self.options).run())

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        parts_dir = mkdtemp()
        self.options['location'] = parts_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        with OutputCapture():
            A11yLint(self.options).run()
        file_exists = os.path.isfile(
            os.path.join(parts_dir, 'a11y-lint.log'))
        rmtree(parts_dir)
        self.assertTrue(file_exists)

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        self.given_a_file_in_test_dir('valid.pt', VALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.pt', INVALID_CODE)
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
