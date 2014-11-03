# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import log
from plone.recipe.codeanalysis.utils import normalize_boolean
from plone.recipe.codeanalysis.utils import read_subprocess_output
from tempfile import TemporaryFile

import os


def code_analysis_flake8(options):
    log('title', 'Flake8')

    jenkins = normalize_boolean(options['jenkins'])
    if 'flake8-filesystem' in options:
        flake8_filesystem = normalize_boolean(options['flake8-filesystem'])
    else:
        flake8_filesystem = False

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
        if jenkins:
            output_file_name = os.path.join(options['location'], 'flake8.log')
            output_file = open(output_file_name, 'w+')
        elif flake8_filesystem:
            output_file_name = os.path.join(options['location'], 'flake8.txt')
            output_file = open(output_file_name, 'w+')
        else:
            output_file = TemporaryFile('w+')

        # Wrapper to subprocess.Popen
        try:
            output, return_code = read_subprocess_output(cmd, output_file)
        except OSError:
            log('skip')
            return False
    finally:
        output_file.close()

    if return_code:
        log('failure', output)
        return False
    else:
        log('ok')
        return True
