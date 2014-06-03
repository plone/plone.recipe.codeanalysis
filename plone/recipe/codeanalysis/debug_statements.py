# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files

import sys


def code_analysis_debug_statements(options):
    sys.stdout.write('Debug statements ')

    sys.stdout.flush()

    # Python files
    files = find_files(options, '.*\.py')
    if files:
        total_errors = []
        file_paths = files.strip().split('\n')
        for file_path in file_paths:
            with open(file_path, 'r') as file_handler:
                errors = _python_lines_parser(
                    file_handler.readlines(), file_path)

            if len(errors) > 0:
                total_errors += errors

    # JavaScript files
    files = find_files(options, '.*\.js')
    if not files:
        print('      [\033[00;32m OK \033[0m]')
        return True

    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _javascript_lines_parser(
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


def _python_lines_parser(lines, file_path):
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


def _javascript_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    debug_statements = (
        'console.log',
    )

    for line in lines:
        linenumber += 1

        # allow to skip some methods if the comment // noqa is found
        if line.find('// noqa') != -1:
            continue

        for statement in debug_statements:
            if line.find(statement) != -1:
                errors.append('{0}:{1}: found {2}'.format(
                    file_path,
                    linenumber,
                    statement)
                )

    return errors
