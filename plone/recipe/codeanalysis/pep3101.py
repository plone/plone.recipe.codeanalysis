# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _find_files

import os
import subprocess
import sys
import time


def code_analysis_pep3101(options):
    sys.stdout.write('PEP 3101')
    sys.stdout.flush()

    files = _find_files(options, '.*\.py')
    if not files:
        print('     [\033[00;32m OK \033[0m]')
        return

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        file_handler = open(file_path, 'r')

        errors = _code_analysis_pep3101_lines_parser(
            file_handler.readlines(),
            file_path)

        file_handler.close()

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


def _code_analysis_pep3101_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    # the ( is to catch keyword formatters '%(something)s'
    string_formatters = ('s', 'i', 'p', 'r', '(')

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
