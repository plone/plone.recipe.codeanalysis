# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.check_manifest import CheckManifest
from shutil import rmtree
from tempfile import mkdtemp
import os
import unittest


class CheckManifestTestCase(unittest.TestCase):

    def setUp(self):  # noqa
        self.test_dir = os.path.realpath(mkdtemp())
        self.options = {
            'bin-directory': 'bin',
            'check-manifest': 'True',
            'check-manifest-directory': self.test_dir,
        }
        # when cwd is parts/test
        if os.path.isfile('../../bin/check-manifest'):
            self.options['bin-directory'] = '../../bin'

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def test_check_manifest_cmd(self):
        executable = '{0:s}/check-manifest'.format(
            self.options['bin-directory'])
        self.assertEqual(CheckManifest(self.options).cmd, [executable, '-v', ])

    def test_check_manifest_packages(self):
        self.assertEqual(
            CheckManifest(self.options).packages, set([self.test_dir])
        )
