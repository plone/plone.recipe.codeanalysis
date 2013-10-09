# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _find_files

import subprocess
import sys


def code_analysis_find_untranslated(options):
    sys.stdout.write('Translations ')
    sys.stdout.flush()
    files = _find_files(options, '.*\.pt')
    if not files:
        print('          [\033[00;32m OK \033[0m]')
        return True

    # put all files in a single line
    files = ' '.join(files.strip().split('\n'))
    cmd = [
        options['i18ndude-bin'],
        'find-untranslated',
        files
    ]
    try:
        process = subprocess.Popen(
            cmd,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )
    except OSError:
        print('          [\033[00;31m SKIP \033[0m]')
        return False
    output, err = process.communicate()
    if '-ERROR-' in output:
        print('          [\033[00;31m FAILURE \033[0m]')
        print(output)
        return False
    else:
        print('          [\033[00;32m OK \033[0m]')
        return True
