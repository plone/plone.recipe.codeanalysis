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
        self.options.setdefault('flake8-exclude', 'bootstrap.py,docs,*.egg')
        self.options.setdefault('flake8-complexity', '10')
        # JSHint
        self.options.setdefault('jshint', 'False')
        self.options.setdefault('jshint-bin', 'jshint')
        # CSS Lint
        self.options.setdefault('csslint', 'False')
        self.options.setdefault('csslint-bin', 'csslint')
        # ZPT Lint
        self.options.setdefault('zptlint', 'False')
        self.options.setdefault('zptlint-bin', 'zptlint')
        # Warn about usage of deprecated methods
        self.options.setdefault('deprecated-methods', 'False')
        # utf-8 header
        self.options.setdefault('utf8-header', 'False')

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
        # bin/code-analysis-zptlint
        zc.buildout.easy_install.scripts(
            [(
                self.name + '-zptlint',
                self.__module__,
                'code_analysis_zptlint'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )
        # bin/code-analysis-deprecated-methods
        zc.buildout.easy_install.scripts(
            [(
                self.name + '-deprecated-methods',
                self.__module__,
                'code_analysis_deprecated_methods'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )
        # bin/code-analysis-utf8-header
        zc.buildout.easy_install.scripts(
            [(
                self.name + '-utf8-header',
                self.__module__,
                'code_analysis_utf8_header'
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


def code_analysis_zptlint(options):
    sys.stdout.write("ZPT Lint")
    sys.stdout.flush()

    files = ''
    for suffix in ('pt', 'cpt', 'zpt', ):
        found_files = _find_files(options, '.*\.{0}'.format(suffix))
        if found_files:
            files += found_files

    if len(files) == 0:
        print('               [\033[00;32m OK \033[0m]')
        return

    # put all files in a single line
    files = ' '.join(files.strip().split('\n'))
    cmd = [
        options['zptlint-bin'],
        files,
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if output != '':
        print('          [\033[00;31m FAILURE \033[0m]')
        print(output)
    else:
        print('               [\033[00;32m OK \033[0m]')


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

    msg = '{0}: {1}: found {2} replace it with {3}'

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
