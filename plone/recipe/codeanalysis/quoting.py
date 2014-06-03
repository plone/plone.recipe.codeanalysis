# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log


def code_analysis_prefer_single_quotes(options):
    log('title', 'Double quotes')

    files = find_files(options, '.*\.py')
    if not files:
        log('ok')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _lines_parser(
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


def _lines_parser(lines, file_path):
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
        errors.append('{0}:{1}: found {2} double quotes'.format(
            file_path,
            linenumber,
            double_quotes_count, ))

    return errors
