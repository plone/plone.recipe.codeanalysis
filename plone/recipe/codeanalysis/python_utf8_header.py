# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log


def code_analysis_utf8_header(options):
    log('title', 'Check utf-8 headers')

    files = find_files(options, '.*\.py')
    if not files:
        log('ok')
        return True

    errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:

            lines = file_handler.readlines()
            if len(lines) == 0:
                continue
            elif lines[0].find('coding: utf-8') == -1:
                errors.append('{0}: missing utf-8 header'.format(file_path))

    if len(errors) > 0:
        log('failure')
        for err in errors:
            print(err)
        return False
    else:
        log('ok')
        return True
