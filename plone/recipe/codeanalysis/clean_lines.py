# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log

import re


def _code_analysis_clean_lines_files_finder(options):
    file_paths = set()
    file_paths_excluded = set([''])
    extensions = (
        'py', 'pt', 'zcml', 'xml',  # standard plone extensions
        'js', 'css', 'html',  # html stuff
        'rst', 'txt',  # documentation
    )

    for suffix in extensions:
        found_files = find_files(options, '.*\.{0}'.format(suffix))
        if found_files:
            file_paths = file_paths.union(
                set(found_files.strip().split('\n')))

    if options['clean-lines-exclude']:
        for suffix in extensions:
            found_files = find_files({
                'directory': options['clean-lines-exclude'],
            }, '.*\.{0}'.format(suffix))
            if found_files:
                file_paths_excluded = file_paths_excluded.union(
                    set(found_files.strip().split('\n')))

    # Remove excluded files
    file_paths -= file_paths_excluded
    return file_paths


def code_analysis_clean_lines(options):
    log('title', 'Check clean lines')

    file_paths = _code_analysis_clean_lines_files_finder(options)
    if len(file_paths) == 0:
        log('ok')
        return True

    total_errors = []
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _code_analysis_clean_lines_parser(
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
