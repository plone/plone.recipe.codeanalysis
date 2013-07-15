# -*- coding: utf-8 -*-
"""Recipe codeanalysis"""
import os
import sys
import time
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

        # Set required default options
        self.options.setdefault('directory', '.')
        self.options.setdefault('pre-commit-hook', 'True')
        # Flake 8
        self.options.setdefault('flake8', 'True')
        self.options.setdefault('flake8-ignore', '')
        self.options.setdefault('flake8-exclude', 'bootstrap.py,docs')
        self.options.setdefault('flake8-complexity', '10')
        # JSHint
        self.options.setdefault('jshint', 'False')
        self.options.setdefault('jshint-bin', 'jshint')
        # CSS Lint
        self.options.setdefault('csslint', 'False')
        self.options.setdefault('csslint-bin', 'csslint')

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
            arguments=self.options.__repr__(),
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
            arguments=self.options.__repr__(),
        )
        # bin/code-analysis-csslint
        zc.buildout.easy_install.scripts(
            [(
                self.name + '-csslint',
                self.__module__,
                'code_analysis_csslint'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

    def install_pre_commit_hook(self):
        git_hooks_directory = self.buildout['buildout']['directory'] + \
            '/.git/hooks'
        if not os.path.exists(git_hooks_directory):
            print(
                "Unable to create git pre-commit hook, "
                "this does not seem to be a git repository.")
            return
        output_file = open(git_hooks_directory + '/pre-commit', 'w')
        output_file.write("#!/bin/bash\nbin/code-analysis")
        output_file.close()
        subprocess.call([
            "chmod",
            "775",
            git_hooks_directory + '/pre-commit',
        ])
        print("Install Git pre-commit hook.")


def _find_files(options, regex):
    cmd = [
        'find',
        '-L',
        options['directory'],
        '-regex',
        regex
    ]
    process_files = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    files, err = process_files.communicate()
    return files


def code_analysis(options):
    if options['flake8'] != 'False':
        code_analysis_flake8(options)
    if options['jshint'] != 'False':
        code_analysis_jshint(options)
    if options['csslint'] != 'False':
        code_analysis_csslint(options)


def code_analysis_flake8(options):
    sys.stdout.write("Flake 8 ")
    sys.stdout.flush()
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
    while process.poll() is None:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
    output, err = process.communicate()
    if process.returncode:
        print("          [\033[00;31m FAILURE \033[0m]")
        print(output)
    else:
        print("               [\033[00;32m OK \033[0m]")


def code_analysis_jshint(options):
    sys.stdout.write("JS Hint")
    sys.stdout.flush()
    files = _find_files(options, '.*\.js')
    if not files:
        print("                [\033[00;32m OK \033[0m]")
        return
    cmd = [
        options['jshint-bin'],
        files.replace("\n", "")
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if process.returncode:
        print("           [\033[00;31m FAILURE \033[0m]")
        print(output)
    else:
        print("                [\033[00;32m OK \033[0m]")


def code_analysis_csslint(options):
    sys.stdout.write("CSS Lint")
    sys.stdout.flush()
    files = _find_files(options, '.*\.css')
    if not files:
        print("               [\033[00;32m OK \033[0m]")
        return
    cmd = [
        options['csslint-bin'],
        '--format=compact',
        files.replace("\n", "")
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if output != '':
        print("          [\033[00;31m FAILURE \033[0m]")
        print(output)
    else:
        print("               [\033[00;32m OK \033[0m]")
