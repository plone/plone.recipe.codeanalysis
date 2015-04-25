# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.clean_lines import CleanLines
from plone.recipe.codeanalysis.csslint import CSSLint
from plone.recipe.codeanalysis.debug_statements import DebugStatements
from plone.recipe.codeanalysis.deprecated_aliases import DeprecatedAliases
from plone.recipe.codeanalysis.flake8 import Flake8
from plone.recipe.codeanalysis.i18ndude import I18NDude
from plone.recipe.codeanalysis.imports import Imports
from plone.recipe.codeanalysis.jscs import JSCS
from plone.recipe.codeanalysis.jshint import JSHint
from plone.recipe.codeanalysis.pep3101 import PEP3101
from plone.recipe.codeanalysis.py_hasattr import HasAttr
from plone.recipe.codeanalysis.python_utf8_header import UTF8Headers
from plone.recipe.codeanalysis.quoting import PreferSingleQuotes
from plone.recipe.codeanalysis.zptlint import ZPTLint
import os
import subprocess
import zc.buildout
import zc.recipe.egg


current_dir = os.path.dirname(__file__)
all_checks = [
    Flake8,
    JSHint,
    JSCS,
    CSSLint,
    ZPTLint,
    DeprecatedAliases,
    UTF8Headers,
    CleanLines,
    PreferSingleQuotes,
    PEP3101,
    Imports,
    DebugStatements,
    I18NDude,
    HasAttr,
]


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(
            buildout,
            self.options['recipe'],
            options
        )

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'], name)

        # Set required default options
        self.options.setdefault('directory', '.')
        self.options.setdefault('pre-commit-hook', 'True')
        # Flake 8
        self.options.setdefault('flake8', 'True')
        self.options.setdefault('flake8-ignore', '')
        self.options.setdefault('flake8-exclude', 'bootstrap.py,boostrap-buildout.py,docs,*.egg')  # noqa
        self.options.setdefault('flake8-max-complexity', '10')
        self.options.setdefault('flake8-max-line-length', '79')
        # JSHint
        self.options.setdefault('jshint', 'False')
        self.options.setdefault('jshint-bin', 'jshint')
        self.options.setdefault('jshint-exclude', '')
        # JSCS
        self.options.setdefault('jscs', 'False')
        self.options.setdefault('jscs-bin', 'jscs')
        self.options.setdefault('jscs-exclude', '')
        # CSS Lint
        self.options.setdefault('csslint', 'False')
        self.options.setdefault('csslint-bin', 'csslint')
        # Warn about usage of deprecated aliases
        self.options.setdefault('deprecated-aliases', 'False')
        # XXX: keep compatibility with previous versions
        if self.options['deprecated-aliases'] == 'False':
            self.options.setdefault('deprecated-alias', 'False')
            deprecated_alias = self.options['deprecated-alias']
            if deprecated_alias == 'False':
                self.options.setdefault('deprecated-methods', 'False')
                deprecated_methods = self.options['deprecated-methods']
                if deprecated_methods != 'False':
                    self.options['deprecated-aliases'] = deprecated_methods
            else:
                self.options['deprecated-aliases'] = deprecated_alias
        # utf-8 header
        self.options.setdefault('utf8-header', 'False')
        # clean lines
        self.options.setdefault('clean-lines', 'False')
        self.options.setdefault('clean-lines-exclude', '')
        # Prefer single quotes over double quotes
        self.options.setdefault('prefer-single-quotes', 'False')
        # PEP 3101 (Advanced String Formatting)
        self.options.setdefault('pep3101', 'False')
        # XXX: keep compatibility with previous versions
        if self.options['pep3101'] == 'False':
            self.options.setdefault('string-formatting', 'False')
            if self.options['string-formatting'] != 'False':
                self.options['pep3101'] = self.options['string-formatting']
        # imports
        self.options.setdefault('imports', 'False')
        # Debug statements
        self.options.setdefault('debug-statements', 'False')
        # Jenkins output
        self.options.setdefault('jenkins', 'False')
        self.options.setdefault('flake8-filesystem', 'False')
        # hasattr
        self.options.setdefault('hasattr', 'False')
        # Error codes
        self.options.setdefault('return-status-codes', 'False')
        # Find untranslated strings
        self.options.setdefault('find-untranslated', 'False')
        self.options.setdefault('i18ndude-bin', '')
        # zptlint
        self.options.setdefault('zptlint', 'False')
        self.options.setdefault('zptlint-bin', '')
        # Figure out default output file
        plone_jenkins = os.path.join(
            self.buildout['buildout']['parts-directory'], 'code-analysis'
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

        # XXX: this has to be handled on a better way; what about 'false'?
        if self.options['pre-commit-hook'] != 'False':
            self.install_pre_commit_hook()
        else:
            self.uninstall_pre_commit_hook()

        # Create location
        wd = self.options.get('working-directory', '')
        if not wd:
            wd = self.options['location']
            if os.path.exists(wd):
                assert os.path.isdir(wd)
            else:
                os.mkdir(wd)
        return self.files

    def update(self):
        self.install()

    def install_scripts(self):
        eggs = self.egg.working_set()[1]
        python_buildout = self.buildout['buildout']['python']
        python = self.buildout[python_buildout]['executable']
        directory = self.buildout['buildout']['bin-directory']
        arguments = self.options.__repr__()

        def add_script(cmd, **kwargs):
            zc.buildout.easy_install.scripts(
                [cmd], eggs, python, directory, **kwargs)

        # flake8
        add_script('flake8')
        # bin/code-analysis
        add_script(
            (self.name, self.__module__, 'code_analysis'),
            arguments=arguments
        )
        # others
        for klass in all_checks:
            instance = klass(self.options)

            if not instance.enabled and 'console_script' in klass.__module__:
                continue

            cmd = ('{0}-{1}'.format(self.name, instance.name),
                   klass.__module__, 'console_script')

            add_script(cmd, arguments=arguments)

    def install_pre_commit_hook(self):
        git_hooks_directory = self.buildout['buildout']['directory'] + \
            '/.git/hooks'
        if not os.path.exists(git_hooks_directory):
            print('Unable to create git pre-commit hook, '
                  'this does not seem to be a git repository.')
            return
        with open(git_hooks_directory + '/pre-commit', 'w') as output_file:
            output_file.write('#!/bin/bash\nbin/code-analysis')
        subprocess.call([
            'chmod',
            '775',
            git_hooks_directory + '/pre-commit',
        ])
        print('Install Git pre-commit hook.')

    def uninstall_pre_commit_hook(self):
        git_hooks_directory = self.buildout['buildout']['directory'] + \
            '/.git/hooks'
        try:
            os.remove(git_hooks_directory + '/pre-commit')
        except OSError:
            pass
        print('Uninstall Git pre-commit hook.')


def code_analysis(options):
    status_codes = []
    for klass in all_checks:
        check = klass(options)

        if check.enabled and not check.run():
            status_codes.append(False)

    # Check all status codes and return with exit code 1 if one of the code
    # analysis steps did not return True
    if options['return-status-codes'] != 'False':
        if not all(status_codes):
            print('The command "bin/code-analysis" exited with 1.')
            exit(1)

        print('The command "bin/code-analysis" exited with 0.')
        exit(0)
