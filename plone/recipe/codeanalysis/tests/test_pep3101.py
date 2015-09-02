# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.pep3101 import PEP3101
from plone.recipe.codeanalysis.pep3101 import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
from testfixtures import OutputCapture


class TestPEP3101(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestPEP3101, self).setUp()
        self.options.update({
            'pep3101': 'True',
        })

    def test_analysis_should_return_true_for_no_files(self):
        with OutputCapture():
            self.assertTrue(PEP3101(self.options).run())

    def test_analysis_should_return_true_for_valid_imports(self):
        self.given_a_file_in_test_dir('valid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'print("hello {0:s}".format("world")',
        ]))
        with OutputCapture():
            self.assertTrue(PEP3101(self.options).run())

    def test_analysis_should_return_false_for_invalid__s(self):
        self.given_a_file_in_test_dir('invalid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'print("hello %s" % ("world")',  # noqa
        ]))
        with OutputCapture():
            self.assertFalse(PEP3101(self.options).run())

    def test_analysis_should_return_false_for_invalid__i(self):
        self.given_a_file_in_test_dir('invalid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'print("hello %i" % ("world")',  # noqa
        ]))
        with OutputCapture():
            self.assertFalse(PEP3101(self.options).run())

    def test_analysis_should_return_false_for_invalid__p(self):
        self.given_a_file_in_test_dir('invalid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'print("hello %p" % ("world")',  # noqa
        ]))
        with OutputCapture():
            self.assertFalse(PEP3101(self.options).run())

    def test_analysis_should_return_false_for_invalid__r(self):
        self.given_a_file_in_test_dir('invalid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'print("hello %r" % (self)',  # noqa
        ]))
        with OutputCapture():
            self.assertFalse(PEP3101(self.options).run())

    def test_analysis_should_return_false_for_multiline_invalid(self):
        self.given_a_file_in_test_dir('invalid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'print("hello %s"',
            '% (self)',
        ]))
        with OutputCapture():
            self.assertFalse(PEP3101(self.options).run())

    def test_analysis_its_complicated(self):
        self.given_a_file_in_test_dir('valid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'log("%s is bad", "me")'
        ]))
        with OutputCapture():
            self.assertTrue(PEP3101(self.options).run())

    def test_analysis_should_return_true_for_logs(self):
        self.given_a_file_in_test_dir('valid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'console.log("hello %s", "world")',  # noqa
        ]))
        with OutputCapture():
            self.assertTrue(PEP3101(self.options).run())

    def test_analysis_should_raise_systemexit_0_in_console_script(self):
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '0'):
                console_script(self.options)

    def test_analysis_should_raise_systemexit_1_in_console_script(self):
        self.given_a_file_in_test_dir('invalid.py', '\n'.join([
            '# -*- coding: utf-8 -*-',
            'print("hello %r" % (self)',  # noqa
        ]))
        with OutputCapture():
            with self.assertRaisesRegexp(SystemExit, '1'):
                console_script(self.options)
