# -*- coding: utf-8 -*-
from multiprocessing import Lock
from multiprocessing import Process
from multiprocessing import Value
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
from plone.recipe.codeanalysis.zptlint import ZPTLint
from time import time
import os
import subprocess
import zc.buildout
import zc.recipe.egg


current_dir = os.path.dirname(__file__)
all_checks = [
    CleanLines,
    CSSLint,
    DebugStatements,
    DeprecatedAliases,
    Flake8,
    HasAttr,
    I18NDude,
    Imports,
    JSCS,
    JSHint,
    PEP3101,
    ZPTLint,
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
        self.options.setdefault('multiprocessing', 'False')
        self.options.setdefault('pre-commit-hook', 'True')
        # Flake 8
        self.options.setdefault('flake8', 'True')
        self.options.setdefault('flake8-extensions', '')
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
        if not bool_option(self.options['deprecated-aliases']):
            self.options.setdefault('deprecated-alias', 'False')
            deprecated_alias = self.options['deprecated-alias']
            if not bool_option(deprecated_alias):
                self.options.setdefault('deprecated-methods', 'False')
                deprecated_methods = self.options['deprecated-methods']
                if bool_option(deprecated_methods):
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
        if not bool_option(self.options['pep3101']):
            self.options.setdefault('string-formatting', 'False')
            if bool_option(self.options['string-formatting']):
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
        self.install_extensions()

        if bool_option(self.options['pre-commit-hook']):
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

    @property
    def extensions(self):
        extensions = self.options['flake8-extensions'].splitlines()
        if bool_option(self.options['flake8']):
            extensions.insert(0, 'flake8>=2.0.0')
        return extensions

    def install_extensions(self):
        for extension in self.extensions:
            zc.recipe.egg.Egg(self.buildout, extension, self.options)

    def install_scripts(self):
        eggs = self.egg.working_set(extra=self.extensions)[1]
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
    start = time()
    multiprocessing = bool_option(options.get('multiprocessing'))
    lock = Lock() if multiprocessing else None
    status = Value('i', 0)

    def taskrunner(klass, options, lock, status):
        check = klass(options, lock)
        if check.enabled:
            if check.run():
                status.value += 1
        else:
            status.value += 1

    if multiprocessing:
        procs = [
            Process(target=taskrunner, args=(klass, options, lock, status))
            for klass in all_checks
        ]
        [p.start() for p in procs]
        [p.join() for p in procs]
    else:
        for klass in all_checks:
            taskrunner(klass, options, lock, status)

    # Check all status codes and return with exit code 1 if one of the code
    # analysis steps did not return True
    if bool_option(options['return-status-codes']):
        exit_code = int(not status.value == len(all_checks))

        print('The command "bin/code-analysis" exited with {0:d} in {1:.03f}s.'
              .format(exit_code, time() - start))
        exit(exit_code)


def bool_option(value):
    return value in ('True', 'true', 'on')
