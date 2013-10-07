# -*- coding: utf-8 -*-
"""Recipe codeanalysis"""
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from plone.recipe.codeanalysis.debug_statements import \
    code_analysis_debug_statements
from plone.recipe.codeanalysis.flake8 import code_analysis_flake8
from plone.recipe.codeanalysis.i18n import code_analysis_find_untranslated
from plone.recipe.codeanalysis.imports import code_analysis_imports
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from plone.recipe.codeanalysis.pep3101 import code_analysis_pep3101
from plone.recipe.codeanalysis.python_utf8_header import \
    code_analysis_utf8_header
from plone.recipe.codeanalysis.quoting import \
    code_analysis_prefer_single_quotes
from plone.recipe.codeanalysis.utils import _find_files
from plone.recipe.codeanalysis.zptlint import code_analysis_zptlint

import os
import re
import subprocess
import sys
import zc.buildout
import zc.recipe.egg


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

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'], name)

        # Set required default options
        self.options.setdefault('directory', '.')
        self.options.setdefault('pre-commit-hook', 'True')
        # Flake 8
        self.options.setdefault('flake8', 'True')
        self.options.setdefault('flake8-ignore', '')
        self.options.setdefault('flake8-exclude', 'bootstrap.py,docs,*.egg')
        self.options.setdefault('flake8-max-complexity', '10')
        self.options.setdefault('flake8-max-line-length', '79')
        # JSHint
        self.options.setdefault('jshint', 'False')
        self.options.setdefault('jshint-bin', 'jshint')
        self.options.setdefault('jshint-exclude', '')
        # CSS Lint
        self.options.setdefault('csslint', 'False')
        self.options.setdefault('csslint-bin', 'csslint')
        # ZPT Lint
        self.options.setdefault('zptlint', 'False')
        self.options.setdefault('zptlint-bin', os.path.join(
            self.buildout['buildout']['bin-directory'], 'zptlint'
        ))
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
        # Error codes
        self.options.setdefault('return-status-codes', 'False')
        # Find untranslated strings
        self.options.setdefault('find-untranslated', 'False')
        i18ndude_path = os.path.join(
            self.buildout['buildout']['bin-directory'], 'i18ndude'
        )
        self.options.setdefault('i18ndude-bin', i18ndude_path)

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
        # data for all scripts
        scripts = [
            # bin/code-analysis
            {'bin': (self.name,
                     self.__module__,
                     'code_analysis'), },
            # flake8
            {'bin': 'flake8',
             'arguments': False, },
            # zptlint
            {'bin': 'zptlint',
             'arguments': False, },
            # bin/code-analysis-flake8
            {'suffix': 'flake8', },
            # bin/code-analysis-jshint
            {'suffix': 'jshint', },
            # bin/code-analysis-csslint
            {'suffix': 'csslint', },
            # bin/code-analysis-zptlint
            {'suffix': 'zptlint', },
            # bin/code-analysis-deprecated-aliases
            {'suffix': 'deprecated-aliases', },
            # bin/code-analysis-utf8-header
            {'suffix': 'utf8-header', },
            # bin/code-analysis-clean-lines
            {'suffix': 'clean-lines', },
            # bin/code-analysis-prefer-single-quotes
            {'suffix': 'prefer-single-quotes', },
            # bin/code-analysis-pep3101
            {'suffix': 'pep3101', },
            # bin/code-analysis-imports
            {'suffix': 'imports', },
            # bin/code-analysis-debug-statements
            {'suffix': 'debug-statements', },
            # bin/code-analysis-find-untranslated
            {'suffix': 'find-untranslated', },
        ]

        eggs = self.egg.working_set()[1]
        python_buildout = self.buildout['buildout']['python']
        python = self.buildout[python_buildout]['executable']
        directory = self.buildout['buildout']['bin-directory']
        arguments = self.options.__repr__()

        for script in scripts:
            cmd = None
            if 'suffix' in script:
                suffix = script['suffix']
                py_method = suffix.replace('-', '_')

                cmd = ('{0}-{1}'.format(self.name, suffix),
                       self.__module__,
                       'code_analysis_{0}'.format(py_method), )
            elif 'bin' in script:
                cmd = script['bin']
            else:
                raise ValueError('Error trying to install a script. Either'
                                 '"bin" or "suffix" are required.')

            if 'arguments' in script and not script['arguments']:
                zc.buildout.easy_install.scripts(
                    [cmd],
                    eggs,
                    python,
                    directory,
                )
            else:
                zc.buildout.easy_install.scripts(
                    [cmd],
                    eggs,
                    python,
                    directory,
                    arguments=arguments,
                )

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
    checks = [
        ['flake8', code_analysis_flake8],
        ['jshint', code_analysis_jshint],
        ['csslint', code_analysis_csslint],
        ['zptlint', code_analysis_zptlint],
        ['deprecated-aliases', code_analysis_deprecated_aliases],
        ['utf8-header', code_analysis_utf8_header],
        ['clean-lines', code_analysis_clean_lines],
        ['prefer-single-quotes', code_analysis_prefer_single_quotes],
        ['pep3101', code_analysis_pep3101],
        ['imports', code_analysis_imports],
        ['debug-statements', code_analysis_debug_statements],
        ['find-untranslated', code_analysis_find_untranslated],
    ]
    status_codes = []
    for option, check in checks:
        if option in options and options[option] != 'False':
            status_codes.append(check(options))

    # Check all status codes and return with exit code 1 if one of the code
    # analysis steps did not return True
    if options['return-status-codes'] != 'False':
        for status_code in status_codes:
            if not status_code:
                print('The command "bin/code-analysis" exited with 1.')
                exit(1)
        print('The command "bin/code-analysis" exited with 0.')
        exit(0)


def code_analysis_deprecated_aliases(options):
    sys.stdout.write('Deprecated aliases')
    sys.stdout.flush()

    # XXX: advice on usage of the right option
    if options.get('deprecated-methods', 'False') != 'False':
        sys.stdout.write('\ndeprecated-methods option is deprecated; '
                         'use deprecated-aliases instead.')
    if options.get('deprecated-alias', 'False') != 'False':
        sys.stdout.write('\ndeprecated-alias option is deprecated; '
                         'use deprecated-aliases instead.')

    files = _find_files(options, '.*\.py')
    if not files:
        print('      [\033[00;32m OK \033[0m]')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _code_analysis_deprecated_aliases_lines_parser(
                file_handler.readlines(), file_path)

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('      [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
        return False
    else:
        print('      [\033[00;32m OK \033[0m]')
        return True


def _code_analysis_deprecated_aliases_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    # Keep adding deprecated aliases and its newer counterparts as:
    # NEWER_VERSION : (LIST OF OLD METHODS)
    deprecated_aliases = {
        'assertEqual': ('failUnlessEqual', 'assertEquals', ),  # noqa
        'assertNotEqual': ('failIfEqual', ),  # noqa
        'assertTrue': ('failUnless', 'assert_', ),  # noqa
        'assertFalse': ('failIf', ),  # noqa
        'assertRaises': ('failUnlessRaises', ),  # noqa
        'assertAlmostEqual': ('failUnlessAlmostEqual', ),  # noqa
        'assertNotAlmostEqual': ('failIfAlmostEqual', ),  # noqa
    }

    msg = '{0}:{1}: found {2} replace it with {3}'

    for line in lines:
        linenumber += 1

        # allow to skip some methods if the comment # noqa is found
        if line.find('# noqa') != -1:
            continue

        for newer_version, old_alias in deprecated_aliases.iteritems():
            for alias in old_alias:
                if line.find(alias) != -1:
                    errors.append(msg.format(
                        file_path,
                        linenumber,
                        alias,
                        newer_version)
                    )
                    continue

    return errors


def code_analysis_clean_lines(options):
    sys.stdout.write('Check clean lines ')
    sys.stdout.flush()

    files = ''
    for suffix in ('py', 'pt', 'zcml', 'xml',  # standard plone extensions
                   'js', 'css', 'html',  # html stuff
                   'rst', 'txt',  # documentation
                   ):
        found_files = _find_files(options, '.*\.{0}'.format(suffix))
        if found_files:
            files += found_files

    if len(files) == 0:
        print('     [\033[00;32m OK \033[0m]')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _code_analysis_clean_lines_parser(
                file_handler.readlines(), file_path)

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('     [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
        return False
    else:
        print('     [\033[00;32m OK \033[0m]')
        return True


def _code_analysis_clean_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    trailing_spaces = re.compile(r' $')
    tabs = re.compile(r'\t')

    for line in lines:
        linenumber += 1

        if trailing_spaces.search(line):
            errors.append('{0}:{1}: found trailing spaces'.format(
                file_path,
                linenumber, ))
        if tabs.search(line):
            errors.append('{0}:{1}: found tabs'.format(
                file_path,
                linenumber, ))
    return errors
