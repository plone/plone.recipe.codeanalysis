# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log

import subprocess


def code_analysis_find_untranslated(options):
    log('title', 'Translations')
    files = find_files(options, '.*\.pt')
    if not files:
        log('ok')
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
        log('skip')
        return False
    output, err = process.communicate()
    if '-ERROR-' in output:
        log('failure', output)
        return False
    else:
        log('ok')
        return True
