# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _find_files

import sys


def code_analysis_utf8_header(options):
    sys.stdout.write('Check utf-8 headers ')
    sys.stdout.flush()

    files = _find_files(options, '.*\.py')
    if not files:
        print('   [\033[00;32m OK \033[0m]')
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
        print('   [\033[00;31m FAILURE \033[0m]')
        for err in errors:
            print(err)
        return False
    else:
        print('   [\033[00;32m OK \033[0m]')
        return True
