# -*- coding: utf-8 -*-
"""Recipe codeanalysis"""
from plone.recipe.codeanalysis.clean_lines import code_analysis_clean_lines
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from plone.recipe.codeanalysis.debug_statements import \
    code_analysis_debug_statements
from plone.recipe.codeanalysis.deprecated_aliases import \
    code_analysis_deprecated_aliases
from plone.recipe.codeanalysis.flake8 import code_analysis_flake8
from plone.recipe.codeanalysis.i18ndude import code_analysis_find_untranslated
from plone.recipe.codeanalysis.imports import code_analysis_imports
from plone.recipe.codeanalysis.jscs import code_analysis_jscs
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from plone.recipe.codeanalysis.pep3101 import code_analysis_pep3101
from plone.recipe.codeanalysis.py_hasattr import code_analysis_hasattr
from plone.recipe.codeanalysis.python_utf8_header import \
    code_analysis_utf8_header
from plone.recipe.codeanalysis.quoting import \
    code_analysis_prefer_single_quotes
from plone.recipe.codeanalysis.zptlint import code_analysis_zptlint
import os
import subprocess
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
        # data for all scripts
        scripts = [
            # bin/code-analysis
            {'bin': (self.name,
                     self.__module__,
                     'code_analysis'), },
            # flake8
            {'bin': 'flake8',
             'arguments': False, },
            # bin/code-analysis-flake8
            {'suffix': 'flake8', },
            # bin/code-analysis-jshint
            {'suffix': 'jshint', },
            # bin/code-analysis-jshint
            {'suffix': 'jscs', },
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
            # bin/code-analysis-hasattr
            {'suffix': 'hasattr', },
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
        ['jscs', code_analysis_jscs],
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
        ['hasattr', code_analysis_hasattr],
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
