# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _find_files
import subprocess
import sys


def code_analysis_zptlint(options):
    sys.stdout.write("ZPT Lint")
    sys.stdout.flush()

    files = ''
    for suffix in ('pt', 'cpt', 'zpt', ):
        found_files = _find_files(options, '.*\.{0}'.format(suffix))
        if found_files:
            files += found_files

    if len(files) == 0:
        print('               [\033[00;32m OK \033[0m]')
        return

    # cmd is a sequence of program arguments
    # first argument is child program
    cmd = [options['zptlint-bin']] + files.split()
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if output != '':
        print('          [\033[00;31m FAILURE \033[0m]')
        print(output)
    else:
        print('               [\033[00;32m OK \033[0m]')
