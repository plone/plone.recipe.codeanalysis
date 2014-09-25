# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log
import re

RE_HASATTR = re.compile('(^|.*\s)hasattr\(.+\).*')
RE_NOQA = re.compile('.*\#\s*noqa($|\s.*)')


def code_analysis_hasattr(options):
    log('title', 'hasattr')

    files = find_files(options, '.*\.py')
    if not files:
        log('ok')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _code_analysis_hasattr_lines_parser(
                file_handler.readlines(),
                file_path
            )

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        log('failure')
        for err in total_errors:
            print(err)
        return False

    log('ok')
    return True


def _code_analysis_hasattr_lines_parser(lines, file_path):
    errors = []
    linenumber = 0
    msg = '{0}:{1}: found hasattr'

    for line in lines:
        linenumber += 1
        # if '# noqa' is on the line, ignore it
        if RE_NOQA.match(line):
            continue

        if RE_HASATTR.match(line):
            errors.append(msg.format(
                file_path,
                linenumber
            ))

    return errors
