# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.chameleonlint import ChameleonLint
from plone.recipe.codeanalysis.check_manifest import CheckManifest
from plone.recipe.codeanalysis.clean_lines import CleanLines
from plone.recipe.codeanalysis.csslint import CSSLint
from plone.recipe.codeanalysis.dependencychecker import DependencyChecker
from plone.recipe.codeanalysis.flake8 import Flake8
from plone.recipe.codeanalysis.i18ndude import I18NDude
from plone.recipe.codeanalysis.importchecker import ImportChecker
from plone.recipe.codeanalysis.jscs import JSCS
from plone.recipe.codeanalysis.jshint import JSHint
from plone.recipe.codeanalysis.scsslint import SCSSLint
from plone.recipe.codeanalysis.xmllint import XMLLint
from plone.recipe.codeanalysis.zptlint import ZPTLint
from time import time

import argparse
import os
import subprocess
import zc.buildout
import zc.recipe.egg


current_dir = os.path.dirname(__file__)
all_checks = [
    ChameleonLint,
    CSSLint,
    CheckManifest,
    CleanLines,
    DependencyChecker,
    ImportChecker,
    Flake8,
    I18NDude,
    JSCS,
    JSHint,
    SCSSLint,
    XMLLint,
    ZPTLint,
]


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(
            buildout,
            self.options['recipe'],
            options,
        )

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'], name,
        )

        # Set required default options
        self.options.setdefault('directory', '.')
        self.options.setdefault('multiprocessing', 'False')
        self.options.setdefault('pre-commit-hook', 'True')
        self.options.setdefault('pre-push-hook', 'False')
        # Flake 8
        self.options.setdefault('flake8', 'True')
        self.options.setdefault('flake8-extensions', '')
        # JSHint
        self.options.setdefault('jshint', 'False')
        self.options.setdefault('jshint-bin', 'jshint')
        self.options.setdefault('jshint-exclude', '')
        self.options.setdefault('jshint-suppress-warnings', 'True')
        # JSCS
        self.options.setdefault('jscs', 'False')
        self.options.setdefault('jscs-bin', 'jscs')
        self.options.setdefault('jscs-exclude', '')
        # Chameleon Lint
        self.options.setdefault('chameleon-lint', 'False')
        # CSS Lint
        self.options.setdefault('csslint', 'False')
        self.options.setdefault('csslint-bin', 'csslint')
        # check-manifest
        self.options.setdefault('check-manifest', 'False')
        self.options.setdefault('check-manifest-directory', '.')
        # clean lines
        self.options.setdefault('clean-lines', 'False')
        self.options.setdefault('clean-lines-exclude', '')
        # dependencychecker
        self.options.setdefault('dependencychecker', 'False')
        self.options.setdefault('dependencychecker-bin', 'dependencychecker')
        # importchecker
        self.options.setdefault('importchecker', 'False')
        self.options.setdefault('importchecker-bin', 'importchecker')
        # Jenkins output
        self.options.setdefault('jenkins', 'False')
        self.options.setdefault('flake8-filesystem', 'False')
        # Error codes
        self.options.setdefault('return-status-codes', 'False')
        self.options.setdefault('pre-commit-return-status-codes',
                                self.options.get('return-status-codes'))
        self.options.setdefault('pre-push-return-status-codes',
                                self.options.get('return-status-codes'))
        # Find untranslated strings
        self.options.setdefault('find-untranslated', 'False')
        self.options.setdefault('i18ndude-bin', '')
        # scss-lint
        self.options.setdefault('scsslint', 'False')
        self.options.setdefault('scsslint-bin', 'scss-lint')
        self.options.setdefault('scsslint-config', '')
        # xmllint
        self.options.setdefault('xmllint', 'False')
        # zptlint
        self.options.setdefault('zptlint', 'False')
        self.options.setdefault('zptlint-bin', '')

        # support user-local overrides from e.g. ~/.buildout/default.cfg
        overrides = self.options.get('overrides')
        overrides_allowed = self.options.get('overrides-allowed', '')
        # except when hard-excluded at the project level buildout.cfg
        if overrides and overrides not in ('False', 'false', '0', 'None'):
            override_options = self.buildout.get(overrides)
            if override_options:
                for (key, value) in override_options.items():
                    if overrides_allowed == '' or key in overrides_allowed:
                        self.options[key] = value

        # Figure out default output file
        plone_jenkins = os.path.join(
            self.buildout['buildout']['parts-directory'], 'code-analysis',
        )
        if not os.path.exists(plone_jenkins):
            os.makedirs(plone_jenkins)

        # What files are tracked by this recipe
        self.files = [
            plone_jenkins,
            os.path.join(
                self.buildout['buildout']['bin-directory'], self.name,
            ),
        ]

    def install(self):
        self.install_scripts()
        self.install_extensions()

        if bool_option(self.options['pre-commit-hook']):
            self.install_hook('pre-commit')
        else:
            self.uninstall_hook('pre-commit')

        if bool_option(self.options['pre-push-hook']):
            self.install_hook('pre-push')
        else:
            self.uninstall_hook('pre-push')

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
        extensions = []
        if bool_option(self.options['flake8']):
            extensions.append('flake8>=2.0.0')
            for item in self.options['flake8-extensions'].splitlines():
                extension = item.strip()
                if extension:
                    extensions.append(extension)
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
                [cmd],
                eggs,
                python,
                directory,
                **kwargs  # noqa: C815 - need py2 backcompatibility
            )

        # flake8
        add_script('flake8')
        # check-manifest
        add_script('check-manifest')
        # bin/code-analysis
        add_script(
            (self.name, self.__module__, 'code_analysis'),
            arguments=arguments,
        )
        # isort
        if 'flake8-isort' in self.extensions:
            add_script('isort')

        # others
        for klass in all_checks:
            instance = klass(self.options)

            if not instance.enabled and 'console_script' in klass.__module__:
                continue

            cmd = (
                '{0}-{1}'.format(self.name, instance.name),
                klass.__module__, 'console_script',
            )

            add_script(cmd, arguments=arguments)

    def install_hook(self, name):
        git_directory = self.buildout['buildout']['directory'] + '/.git'
        if not os.path.exists(git_directory):
            print(
                'Unable to create git {0} hook, '
                'this does not seem to be a git repository.'.format(name))
            return

        git_hooks_directory = git_directory + '/hooks'
        if not os.path.exists(git_hooks_directory):
            os.mkdir(git_hooks_directory)

        hook = git_hooks_directory + '/' + name
        with open(hook, 'w') as output_file:
            output_file.write('#!/usr/bin/env bash\nbin/code-analysis')
            # 'pre-commit-return-status-codes' and
            # 'pre-push-return-status-codes', if unset, inherit
            # their values from vanilla 'return-status-codes'
            if bool_option(self.options[
                    '{0}-return-status-codes'.format(name)]):
                output_file.write(' --return-status-codes')
            else:
                output_file.write(' --no-return-status-codes')
        subprocess.call([
            'chmod',
            '775',
            hook,
        ])
        print('Installed Git {0} hook.'.format(name))

    def uninstall_hook(self, name):
        git_hooks_directory = self.buildout['buildout']['directory'] + \
            '/.git/hooks'
        try:
            hook = git_hooks_directory + '/' + name
            os.remove(hook)
        except OSError:
            pass
        print('Uninstalled Git {0} hook.'.format(name))


def parse_command_line_arguments(options):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'directory', nargs='?',
        help='Directory to run code-analysis on. Defaults to cwd.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-x', '--return-status-codes',
        action='store_true',
        help=('Exit with code 1 on validation errors,'
              ' overrides buildout.cfg default.'),
    )
    group.add_argument(
        '-n', '--no-return-status-codes',
        action='store_true',
        help=('Always exit with code 0, even on validation errors.'
              ' Overrides buildout.cfg default.'),
    )

    args = parser.parse_args()
    if args.directory:
        options['directory'] = args.directory
        options['check-manifest-directory'] = args.directory
    if args.return_status_codes:
        options['return-status-codes'] = True
    if args.no_return_status_codes:
        options['return-status-codes'] = False

    return options


def code_analysis(options):
    start = time()
    options = parse_command_line_arguments(options)

    class DummyValue(object):
        def __init__(self, value=True):
            self.value = value

    lock = None
    status = DummyValue()
    multiprocessing = bool_option(options.get('multiprocessing'))

    def taskrunner(klass, options, lock, status):
        check = klass(options, lock)
        if check.enabled:
            if not check.run():
                status.value = False

    if multiprocessing:
        from multiprocessing import Lock
        from multiprocessing import Process
        from multiprocessing import Value

        lock = Lock()
        status = Value('b', True)
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
        exit_code = 0 if status.value else 1

        print('The command "bin/code-analysis" exited with {0:d} in {1:.03f}s.'
              .format(exit_code, time() - start))
        exit(exit_code)


def bool_option(value):
    return value in (True, 'True', 'true', 'on')
