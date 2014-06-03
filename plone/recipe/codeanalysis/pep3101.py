# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log

import sys


def code_analysis_pep3101(options):
    log('title', 'PEP 3101')

    # XXX: advice on usage of the right option
    if options.get('string-formatting', 'False') != 'False':
        sys.stdout.write('\nstring-formatting option is deprecated; '
                         'use pep3101 instead.')

    files = find_files(options, '.*\.py')
    if not files:
        log('ok')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _code_analysis_pep3101_lines_parser(
                file_handler.readlines(), file_path)

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        log('failure')
        for err in total_errors:
            print(err)
        return False
    else:
        log('ok')
        return True


def _code_analysis_pep3101_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    # FIXME: following line demonstrates the parser is buggy (refs. #29)
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
