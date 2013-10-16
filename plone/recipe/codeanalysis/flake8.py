# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _normalize_boolean
from utils import log

import os
import subprocess


def code_analysis_flake8(options):
    log('title', 'Flake8')
    jenkins = _normalize_boolean(options['jenkins'])

    # cmd is a sequence of program arguments
    # first argument is child program
    cmd = [
        os.path.join(options['bin-directory']) + '/flake8',
        '--ignore={0}'.format(options['flake8-ignore']),
        '--exclude={0}'.format(options['flake8-exclude']),
        '--max-complexity={0}'.format(options['flake8-max-complexity']),
        '--max-line-length={0}'.format(options['flake8-max-line-length'])
    ]

    paths_to_check = options['directory'].split('\n')
    cmd.extend(paths_to_check)

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
    if jenkins:
        log_filename = os.path.join(options['location'], 'flake8.log')
        with open(log_filename, 'w') as flake8_log:
            flake8_log.write(output)
    if process.returncode:
        log('failure', output)
        return False
    else:
        log('ok')
        return True
