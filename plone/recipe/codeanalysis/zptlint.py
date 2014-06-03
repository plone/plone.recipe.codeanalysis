# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log

import subprocess


def code_analysis_zptlint(options):
    log('title', 'ZPT Lint')

    files = ''
    for suffix in ('pt', 'cpt', 'zpt', ):
        found_files = find_files(options, '.*\.{0}'.format(suffix))
        if found_files:
            files += found_files

    if len(files) == 0:
        log('ok')
        return True

    # cmd is a sequence of program arguments
    # first argument is child program
    cmd = [options['zptlint-bin']] + files.split()
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
    if output != '':
        log('failure', output)
        return False
    else:
        log('ok')
        return True
