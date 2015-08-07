# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis import Recipe
from shutil import rmtree
from tempfile import mkdtemp
from testfixtures import OutputCapture

import os
import unittest


class RecipeTestCase(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.realpath(mkdtemp())
        for directory in ('bin', 'parts', 'eggs', 'develop-eggs', ):
            os.makedirs('{0}/{1}'.format(test_dir, directory))

        self.buildout_options = {
            'buildout': {
                'bin-directory': '{0}/bin'.format(test_dir),
                'parts-directory': '{0}/parts'.format(test_dir),
                'python': 'buildout',
                'executable': '{0}/bin/python2.7'.format(test_dir),
                'directory': '{0}'.format(test_dir),
                'find-links': '',
                'allow-hosts': '*',
                'eggs-directory': '{0}/eggs'.format(test_dir),
                'develop-eggs-directory': '{0}/develop-eggs'.format(test_dir),
            },
        }
        self.test_dir = test_dir
        self.options = {
            'recipe': 'plone.recipe.codeanalysis',
        }
        self.name = 'code-analysis'
        self.code_analysis = self._get_recipe()

    def tearDown(self):  # noqa
        rmtree(self.test_dir)

    def _get_recipe(self, buildout_options=None, name=None, options=None):
        if buildout_options is None:
            buildout_options = self.buildout_options
        if name is None:
            name = self.name
        if options is None:
            options = self.options
        return Recipe(
            buildout_options,
            name,
            options
        )

    def test_minimal_options(self):
        code_analysis = self._get_recipe(None, None, None)
        self.assertTrue(code_analysis)

    def test_egg(self):
        self.assertTrue(self.code_analysis.egg)

    def test_location(self):
        location = '{0}/{1}'.format(
            self.buildout_options['buildout']['parts-directory'],
            self.name
        )
        self.assertEqual(
            self.code_analysis.options['location'],
            location
        )

    def test_jenkins_path(self):
        jenkins_path = '{0}/code-analysis'.format(
            self.buildout_options['buildout']['parts-directory'],
        )
        self.assertTrue(os.path.exists(jenkins_path))

    def test_recipe_files(self):
        jenkins_path = '{0}/code-analysis'.format(
            self.buildout_options['buildout']['parts-directory'],
        )
        location = '{0}/{1}'.format(
            self.buildout_options['buildout']['parts-directory'],
            self.name
        )
        self.assertIn(jenkins_path, self.code_analysis.files)
        self.assertIn(location, self.code_analysis.files)

    def test_no_git_folder(self):
        with OutputCapture() as out:
            self.code_analysis.install_pre_commit_hook()
            found = out.captured.find('Unable to create git pre-commit hook,')
            self.assertTrue(found == 0)

    def test_hooks_folder_being_created(self):
        os.makedirs('{0}/.git'.format(self.test_dir))
        with OutputCapture() as out:
            self.code_analysis.install_pre_commit_hook()
            out.compare('Install Git pre-commit hook.')
        self.assertTrue(os.path.exists('{0}/.git/hooks'.format(self.test_dir)))

    def test_hook_file_exists(self):
        os.makedirs('{0}/.git/hooks'.format(self.test_dir))
        with OutputCapture() as out:
            self.code_analysis.install_pre_commit_hook()
            out.compare('Install Git pre-commit hook.')
        self.assertTrue(
            os.path.exists('{0}/.git/hooks/pre-commit'.format(self.test_dir))
        )

    def test_hook_contents(self):
        os.makedirs('{0}/.git/hooks'.format(self.test_dir))
        with OutputCapture():
            self.code_analysis.install_pre_commit_hook()

        with open('{0}/.git/hooks/pre-commit'.format(self.test_dir)) as f:
            file_contents = f.read()

        self.assertTrue(file_contents.find('bin/code-analysis') != -1)

    def test_uninstall_hook(self):
        os.makedirs('{0}/.git/hooks'.format(self.test_dir))
        with open('{0}/.git/hooks/pre-commit'.format(self.test_dir), 'w') as f:
            f.write('something')

        with OutputCapture() as output:
            self.code_analysis.uninstall_pre_commit_hook()
            output.compare('Uninstall Git pre-commit hook.')

    def test_uninstall_hook_no_os_error(self):
        os.makedirs('{0}/.git/hooks'.format(self.test_dir))

        with OutputCapture() as output:
            self.code_analysis.uninstall_pre_commit_hook()
            output.compare('Uninstall Git pre-commit hook.')

    def test_extensions_default(self):
        self.assertEqual(
            self.code_analysis.extensions,
            ['flake8>=2.0.0', ]
        )

    def test_extensions_no_flake8(self):
        self.options['flake8'] = False
        self.code_analysis = self._get_recipe()
        self.assertEqual(self.code_analysis.extensions, [])

    def test_extensions_flake8_plugins(self):
        self.options['flake8-extensions'] = 'pep8-naming\nflake8-todo'
        self.code_analysis = self._get_recipe()
        self.assertEqual(
            self.code_analysis.extensions,
            ['flake8>=2.0.0', 'pep8-naming', 'flake8-todo']
        )

    def test_extensions_flake8_empty_plugins(self):
        self.options['flake8-extensions'] = '\n\n'
        self.code_analysis = self._get_recipe()
        self.assertEqual(
            self.code_analysis.extensions,
            ['flake8>=2.0.0', ]
        )
