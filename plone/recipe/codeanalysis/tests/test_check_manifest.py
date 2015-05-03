# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.check_manifest import CheckManifest
from plone.recipe.codeanalysis.check_manifest import console_script
from plone.recipe.codeanalysis.testing import CodeAnalysisTestCase
import os


class TestCheckManifest(CodeAnalysisTestCase):

    def setUp(self):  # noqa
        super(TestCheckManifest, self).setUp()
        self.options.update({
            'check-manifest': 'True',
            'check-manifest-directory': self.test_dir,
        })
        # when cwd is parts/test
        if os.path.isfile('../../bin/check-manifest'):
            self.options['bin-directory'] = '../../bin'

    def test_check_manifest_cmd(self):
        executable = '{0:s}/check-manifest'.format(
            self.options['bin-directory']
        )
        self.assertEqual(CheckManifest(self.options).cmd, [executable, '-v', ])

    def test_check_manifest_packages(self):
        self.assertEqual(
            CheckManifest(self.options).packages, set([self.test_dir])
        )

    def test_check_manifest_should_return_true_on_this_package(self):
        self.options['check-manifest-directory'] = os.path.realpath(
            os.path.join(os.path.dirname(__file__), '../../../..')
        )
        self.assertTrue(CheckManifest(self.options).run())

    def test_check_manifest_should_return_true_if_no_check_manifest_installed(self):  # noqa
        self.options['bin-directory'] = ''
        self.assertTrue(CheckManifest(self.options).run())

    def test_check_manifest_should_raise_systemexit_0_in_console_script(self):
        self.options['check-manifest-directory'] = os.path.realpath(
            os.path.join(os.path.dirname(__file__), '../../../..')
        )
        with self.assertRaisesRegexp(SystemExit, '0'):
            console_script(self.options)

    def test_check_manifest_should_raise_systemexit_1_in_console_script(self):
        with self.assertRaisesRegexp(SystemExit, '1'):
            console_script(self.options)
