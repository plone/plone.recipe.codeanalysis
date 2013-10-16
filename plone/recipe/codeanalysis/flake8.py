# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _normalize_boolean

import os
import subprocess
import sys


def code_analysis_flake8(options):
    sys.stdout.write('Flake8')
    sys.stdout.flush()
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
        print('              [\033[00;31m SKIP \033[0m]')
        return False
    output, err = process.communicate()
    if jenkins:
        log_filename = os.path.join(options['location'], 'flake8.log')
        with open(log_filename, 'w') as flake8_log:
            flake8_log.write(output)
    if process.returncode:
        print('            [\033[00;31m FAILURE \033[0m]')
        print(output)
        return False
    else:
        print('                 [\033[00;32m OK \033[0m]')
        return True
