# -*- coding: utf-8 -*-
"""Recipe codeanalysis"""
import os
import sys
import zc.buildout
import zc.recipe.egg

import subprocess
import pep8

from subprocess import Popen, PIPE
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
        self.install_pre_commit_hook()
        return self.files

    def update(self):
        self.install()

    def install_scripts(self):
        zc.buildout.easy_install.scripts(
            [(
                self.name,
                self.__module__,
                'code_analysis'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )
        zc.buildout.easy_install.scripts(
            [(
                self.name + '-flake8',
                self.__module__,
                'code_analysis_flake8'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

    def install_pre_commit_hook(self):
        """Flake8 Python pre-commit hook.
        """
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

    def create_pre_commit_hook(self):
        """Full bash-based pre-commit hook.
        """
        tmpl_filename = os.path.join(current_dir, 'templates', 'pre-commit.sh.tmpl')


def code_analysis(options):
    code_analysis_flake8(options)


def code_analysis_flake8(options):
    print("Flake 8 Code Analysis")
    print("---------------------")
    bin_dir = os.path.join(options['bin-directory'])
    #ignore = 'E226,E302,E41'
    ignore = ''
    output = subprocess.call([bin_dir + '/flake8', '--ignore=%s' % ignore])
    print(output)
    print("---------------------")
