# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log
import re


def code_analysis_imports(options):
    log('title', 'Check imports')
    files = find_files(options, '.*\.py')
    if not files:
        log('ok')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            lines = file_handler.readlines()
            total_errors += _code_analysis_imports_parser(lines, file_path)
            total_errors += _code_analysis_imports_sorting(lines, file_path)

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


def _code_analysis_imports_sorting(lines, relative_path):
    errors = []
    imports = []
    linenumber = 0

    def is_from_import(l):
        return re.match(r'^from\s+([^\s]+)\s+import\s+([^\s]+)$', l)

    def is_module_import(l):
        return re.match(r'^import\s+([^\s]+)$', l)

    previous_line = ''
    for line in lines:
        linenumber += 1

        # allow to skip some methods if the comment # noqa is found
        if line.find('# noqa') != -1:
            continue

        is_multiline_import = line.strip().endswith('\\')
        if is_multiline_import:
            previous_line += line
            continue

        if not is_multiline_import and previous_line:
            line = previous_line.strip('\\\n') + line.strip()
            previous_line = ''

        if is_from_import(line) or is_module_import(line):
            imports.append((linenumber, line))

    # duplicate imports list and sort it
    imports_sorted = imports[:]
    imports_sorted.sort(key=lambda x: x[1])

    if imports_sorted != imports:
        errors.append('{0}:{1}-{2}: found unsorted imports'.format(
            relative_path, imports[0][0], imports[-1][0]))

    return errors
