# -*- coding: utf-8 -*-
"""Recipe codeanalysis"""
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from plone.recipe.codeanalysis.flake8 import code_analysis_flake8
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from plone.recipe.codeanalysis.zptlint import code_analysis_zptlint
from plone.recipe.codeanalysis.utils import _find_files

import os
import re
import sys
import zc.buildout
import zc.recipe.egg

import subprocess

current_dir = os.path.dirname(__file__)

# XXX: see http://2002-2012.mattwilcox.net/archive/entry/id/1054/
CSSLINT_IGNORE = ','.join([
    'adjoining-classes',
    'floats',
    'font-faces',
    'font-sizes',
    'ids',
    'qualified-headings',
    'unique-headings',
])


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
        self.options.setdefault('csslint-bin', os.path.join(
            self.buildout['buildout']['bin-directory'], 'csslint'
        ))
        # ZPT Lint
        self.options.setdefault('zptlint', 'False')
        self.options.setdefault('zptlint-bin', os.path.join(
            self.buildout['buildout']['bin-directory'], 'zptlint'
        ))
        # Warn about usage of deprecated methods
        self.options.setdefault('deprecated-methods', 'False')
        # utf-8 header
        self.options.setdefault('utf8-header', 'False')
        # clean lines
        self.options.setdefault('clean-lines', 'False')
        # Prefer single quotes over double quotes
        self.options.setdefault('prefer-single-quotes', 'False')
        # String formatting
        self.options.setdefault('string-formatting', 'False')
        # imports
        self.options.setdefault('imports', 'False')
        # Debug statements
        self.options.setdefault('debug-statements', 'False')
        # Jenkins output
        self.options.setdefault('jenkins', 'False')

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
            # bin/code-analysis-deprecated-methods
            {'suffix': 'deprecated-methods', },
            # bin/code-analysis-utf8-header
            {'suffix': 'utf8-header', },
            # bin/code-analysis-clean-lines
            {'suffix': 'clean-lines', },
            # bin/code-analysis-prefer-single-quotes
            {'suffix': 'prefer-single-quotes', },
            # bin/code-analysis-string-formatting
            {'suffix': 'string-formatting', },
            # bin/code-analysis-imports
            {'suffix': 'imports', },
            # bin/code-analysis-debug-statements
            {'suffix': 'debug-statements', },
        ]

        # bin/jenkins-code-analysis
        if self.options['jenkins'] == 'True':
            scripts.append({
                'bin': (
                    'jenkins-' + self.name,
                    self.__module__,
                    'jenkins_code_analysis'),
            })
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

    def uninstall_pre_commit_hook(self):
        git_hooks_directory = self.buildout['buildout']['directory'] + \
            '/.git/hooks'
        try:
            os.remove(git_hooks_directory + '/pre-commit')
        except OSError:
            pass
        print("Uninstall Git pre-commit hook.")


def code_analysis(options):
    if 'flake8' in options and options['flake8'] != 'False':
        code_analysis_flake8(options)
    if 'jshint' in options and options['jshint'] != 'False':
        code_analysis_jshint(options)
    if 'csslint' in options and options['csslint'] != 'False':
        code_analysis_csslint(options)
    if 'zptlint' in options and options['zptlint'] != 'False':
        code_analysis_zptlint(options)
    if 'deprecated-methods' in options and \
            options['deprecated-methods'] != 'False':
        code_analysis_deprecated_methods(options)
    if 'utf8-header' in options and options['utf8-header'] != 'False':
        code_analysis_utf8_header(options)
    if 'clean-lines' in options and options['clean-lines'] != 'False':
        code_analysis_clean_lines(options)
    if 'prefer-single-quotes' in options and \
            options['prefer-single-quotes'] != 'False':
        code_analysis_prefer_single_quotes(options)
    if 'string-formatting' in options and \
            options['string-formatting'] != 'False':
        code_analysis_string_formatting(options)
    if 'imports' in options and options['imports'] != 'False':
        code_analysis_imports(options)
    if 'debug-statements' in options and \
            options['debug-statements'] != 'False':
        code_analysis_debug_statements(options)


def jenkins_code_analysis(options):
    pass


def code_analysis_deprecated_methods(options):
    sys.stdout.write('Deprecated methods ')
    sys.stdout.flush()

    files = _find_files(options, '.*\.py')
    if not files:
        print('    [\033[00;32m OK \033[0m]')
        return

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')

        errors = _code_analysis_deprecated_methods_lines_parser(
            file_handler.readlines(),
            file_path)

        file_handler.close()

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('    [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
    else:
        print('    [\033[00;32m OK \033[0m]')


def _code_analysis_deprecated_methods_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    # Keep adding deprecated methods and its newer counterparts as:
    # NEWER_VERSION : (LIST OF OLD METHODS)
    deprecated_methods = {
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

        for newer_version, old_alias in deprecated_methods.iteritems():
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


def code_analysis_utf8_header(options):
    sys.stdout.write('Check utf-8 headers ')
    sys.stdout.flush()

    files = _find_files(options, '.*\.py')
    if not files:
        print('   [\033[00;32m OK \033[0m]')
        return

    errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')

        lines = file_handler.readlines()
        if len(lines) == 0:
            continue
        elif lines[0].find('coding: utf-8') == -1:
            errors.append('{0}: missing utf-8 header'.format(file_path))

        file_handler.close()

    if len(errors) > 0:
        print('   [\033[00;31m FAILURE \033[0m]')
        for err in errors:
            print(err)
    else:
        print('   [\033[00;32m OK \033[0m]')


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
        return

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')

        errors = _code_analysis_clean_lines_parser(
            file_handler.readlines(),
            file_path)

        file_handler.close()

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('     [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
    else:
        print('     [\033[00;32m OK \033[0m]')


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


def code_analysis_prefer_single_quotes(options):
    sys.stdout.write('Double quotes ')
    sys.stdout.flush()

    files = _find_files(options, '.*\.py')
    if not files:
        print('         [\033[00;32m OK \033[0m]')
        return

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')

        errors = _code_analysis_prefer_single_quotes_lines_parser(
            file_handler.readlines(),
            file_path)

        file_handler.close()

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('         [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
    else:
        print('         [\033[00;32m OK \033[0m]')


def _code_analysis_prefer_single_quotes_lines_parser(lines, file_path):
    errors = []
    multiline = False
    linenumber = 0

    for line in lines:
        linenumber += 1

        # if there is no double quote sign
        # there's nothing to do
        if line.find('"') == -1:
            continue

        # if it's a comment line ignore it
        if line.strip().startswith('#'):
            continue

        # if it's a multiline string, is
        # ok to have doublequotes
        if line.find('"""') != -1:
            # don't get trapped on multiline
            # strings that are on a single line
            if line.count('"""') == 2:
                continue
            elif multiline:
                multiline = False
            else:
                multiline = True
            continue

        # until the multiline is finished
        # it doesn't matter if single or
        # double quotes are used
        if multiline:
            continue

        # if in the same line are both single
        # and double quotes, ignore it
        if line.find('"') != -1 and \
                line.find("'") != -1:
            continue

        double_quotes_count = line.count('"')
        errors.append("{0}:{1}: found {2} double quotes".format(
            file_path,
            linenumber,
            double_quotes_count, ))

    return errors


def code_analysis_string_formatting(options):
    sys.stdout.write('String formatting ')
    sys.stdout.flush()

    files = _find_files(options, '.*\.py')
    if not files:
        print('     [\033[00;32m OK \033[0m]')
        return

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')

        errors = _code_analysis_string_formatting_lines_parser(
            file_handler.readlines(),
            file_path)

        file_handler.close()

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('     [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
    else:
        print('     [\033[00;32m OK \033[0m]')


def _code_analysis_string_formatting_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    string_formatters = ('s', 'i', 'p', 'r')

    for line in lines:
        linenumber += 1

        # if '# noqa' is on the line, ignore it
        if line.find('# noqa') != -1:
            continue

        # if there is no formatting
        # going on skip it
        if line.find('%') == -1:
            continue

        # check if it's a formatting string
        for formatter in string_formatters:
            formatter = '%{0}'.format(formatter)
            if line.find(formatter) != -1:
                errors.append('{0}:{1}: found {2} formatter'.format(
                    file_path,
                    linenumber,
                    formatter,
                ))
    return errors


def code_analysis_imports(options):
    sys.stdout.write('Check imports ')
    sys.stdout.flush()
    files = _find_files(options, '.*\.py')
    if not files:
        print('                [\033[00;32m OK \033[0m]')
        return

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')
        errors = _code_analysis_imports_parser(file_handler.readlines(),
                                               file_path)
        file_handler.close()

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('         [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
    else:
        print('         [\033[00;32m OK \033[0m]')


def _code_analysis_imports_parser(lines, relative_path):
    errors = []
    linenumber = 0
    for line in lines:
        linenumber += 1

        if line.find('from ') == 0:
            if line.find(', ') != -1 or line.find(' (') != -1:
                errors.append('{0}:{1}: found grouped imports'.format(
                    relative_path,
                    linenumber,
                ))
    return errors


def code_analysis_debug_statements(options):
    sys.stdout.write('Debug statements ')

    sys.stdout.flush()

    files = _find_files(options, '.*\.py')
    if not files:
        print('      [\033[00;32m OK \033[0m]')
        return

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')

        errors = _code_analysis_debug_statements_lines_parser(
            file_handler.readlines(),
            file_path)

        file_handler.close()

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        print('      [\033[00;31m FAILURE \033[0m]')
        for err in total_errors:
            print(err)
    else:
        print('      [\033[00;32m OK \033[0m]')


def _code_analysis_debug_statements_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    debug_statements = (
        'print',  # noqa
        'pdb',  # noqa
    )

    for line in lines:
        linenumber += 1

        # allow to skip some methods if the comment # noqa is found
        if line.find('# noqa') != -1:
            continue

        for statement in debug_statements:
            if line.find(statement) != -1:
                errors.append('{0}:{1}: found {2}'.format(
                    file_path,
                    linenumber,
                    statement)
                )

    return errors
