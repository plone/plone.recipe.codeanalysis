# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis import Recipe

import os
import unittest


class RecipeTestCase(unittest.TestCase):

    def setUp(self):
        self.buildout_options = {
            'buildout': {
                'bin-directory': '/tmp/buildout/bin',
                'parts-directory': '/tmp/buildout/parts',
                'python': 'buildout',
                'executable': '/tmp/buildout/bin/python2.7',
                'directory': '/tmp/buildout',
                'find-links': '',
                'allow-hosts': '*',
                'eggs-directory': '/home/plone/.buildout/eggs',
                'develop-eggs-directory': '/tmp/buildout/develop-eggs',
            },
        }
        self.options = {
            'recipe': 'plone.recipe.codeanalysis',
        }
        self.name = 'code-analysis'
        self.code_analysis = self._get_recipe(None, None, None)

    def _get_recipe(self, buildout_options, name, options):
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
