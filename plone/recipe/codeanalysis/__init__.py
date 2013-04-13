# -*- coding: utf-8 -*-
"""Recipe codeanalysis"""
import os
import sys
import zc.buildout
import zc.recipe.egg

import pep8

from genshi.template import TextTemplate

current_dir = os.path.dirname(__file__)


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(
            buildout,
            self.options['recipe'],
            options
        )

        # Set default options
        self.options.setdefault('flake8-complexity', '10')
        self.options.setdefault('jslint', 'False')
        self.options.setdefault('csslint', 'False')

        # Figure out default output file
        plone_jenkins = os.path.join(
            self.buildout['buildout']['parts-directory'], __name__
        )
        if not os.path.exists(plone_jenkins):
            os.makedirs(plone_jenkins)

        # What files are tracked by this recipe
        self.files = [
            plone_jenkins,
            os.path.join(
                self.buildout['buildout']['bin-directory'], self.name
            )
        ]

    def install(self):
        self.install_scripts()
        return self.files

    def update(self):
        self.install()

    def install_scripts(self):
        zc.buildout.easy_install.scripts(
            [(
                self.name,
                self.__module__,
                'code_analysis_flake8'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )
        self.create_pre_commit_hook()

    def create_pre_commit_hook(self):
        tmpl_filename = os.path.join(current_dir, 'templates', 'pre-commit.tmpl')
        tmpl_file = open(tmpl_filename, 'r')
        tmpl = TextTemplate(tmpl_file.read())
        tmpl_file.close()
        python_bin = self.buildout['buildout']['bin-directory'] + '/zopepy'
        stream = tmpl.generate(
            python_bin=python_bin
        )
        git_hooks_directory = os.path.join(
            self.buildout['buildout']['directory'],
            '.git/hooks', 
        )
        output_file = open(git_hooks_directory + '/pre-commit', 'w')
        output_file.write(stream.render())
        output_file.close()

def code_analysis_flake8(options):
    pass
