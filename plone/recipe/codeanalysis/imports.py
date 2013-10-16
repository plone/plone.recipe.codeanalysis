# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _find_files
from plone.recipe.codeanalysis.utils import log


def code_analysis_imports(options):
    log('title', 'Check imports')
    files = _find_files(options, '.*\.py')
    if not files:
        log('ok')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _code_analysis_imports_parser(
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
