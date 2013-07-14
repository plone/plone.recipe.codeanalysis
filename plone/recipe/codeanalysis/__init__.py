# -*- coding: utf-8 -*-
"""Recipe codeanalysis"""
import os
import zc.buildout
import zc.recipe.egg

import subprocess

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
        self.options.setdefault('directory', '.')
        self.options.setdefault('pre-commit-hook', 'False')
        self.options.setdefault('flake8-ignore', '')
        self.options.setdefault('flake8-exclude', 'bootstrap.py,docs,src')
        self.options.setdefault('flake8-complexity', '10')
        self.options.setdefault('jshint', 'False')
        self.options.setdefault('jshint-bin', 'jshint')
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
        if self.options['pre-commit-hook'] != 'False':
            self.install_pre_commit_hook()
        return self.files

    def update(self):
        self.install()

    def install_scripts(self):
        # bin/code-analysis
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
        # bin/flake8
        zc.buildout.easy_install.scripts(
            ['flake8'],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
        )
        # bin/code-analysis-flake8
        zc.buildout.easy_install.scripts(
            [(
                self.name + '-flake8',
                self.__module__,
                'code_analysis_flake8'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
        )
        # bin/code-analysis-jshint
        zc.buildout.easy_install.scripts(
            [(
                self.name + '-jshint',
                self.__module__,
                'code_analysis_jshint'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
        )

    def install_pre_commit_hook(self):
        """Flake8 Python pre-commit hook.
        """
        tmpl_filename = os.path.join(
            current_dir,
            'templates',
            'pre-commit.tmpl'
        )
        tmpl_file = open(tmpl_filename, 'r')
        from genshi.template import TextTemplate
        tmpl = TextTemplate(tmpl_file.read())
        tmpl_file.close()
        stream = tmpl.generate(
            buildout_directory=self.buildout['buildout']['directory']
        )
        git_hooks_directory = os.path.join(
            self.buildout['buildout']['directory'],
            '.git/hooks',
        )
        output_file = open(git_hooks_directory + '/pre-commit', 'w')
        output_file.write(stream.render())
        output_file.close()
        subprocess.call([
            "chmod",
            "775",
            git_hooks_directory + '/pre-commit',
        ])


def code_analysis(options):
    code_analysis_flake8(options)
    if options['jshint'] != 'False':
        code_analysis_jshint(options)


def code_analysis_flake8(options):
    cmd = [
        os.path.join(options['bin-directory']) + '/flake8',
        '--ignore=%s' % options['flake8-ignore'],
        '--exclude=%s' % options['flake8-exclude'],
        options['directory'],
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if process.returncode:
        print("Flake 8           [\033[00;31m FAILURE \033[0m]")
        print(output)
    else:
        print("Flake 8                [\033[00;32m OK \033[0m]")


def code_analysis_jshint(options):
    cmd = [
        'find',
        '-L',
        options['directory'],
        '-regex',
        '.*\.js'
    ]
    process_jsfiles = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    jsfiles, err = process_jsfiles.communicate()
    if not jsfiles:
        print("JS Hint                [\033[00;32m OK \033[0m]")
        return
    cmd = [
        options['jshint-bin'],
        jsfiles.replace("\n", "")
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if process.returncode:
        print("JS Hint           [\033[00;31m FAILURE \033[0m]")
        print(output)
    else:
        print("JS Hint                [\033[00;32m OK \033[0m]")
