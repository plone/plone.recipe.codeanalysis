# -*- coding: utf-8 -*-

from plone.recipe.codeanalysis.utils import _normalize_boolean
from plone.recipe.codeanalysis.utils import _process_output

import os
import re
import subprocess
import sys


def jshint_errors(output, jenkins=False):
    """Search for error markers as JSHint always return an exit code of 2
    either if a file has errors or warnings. This method search for markers
    of errors (E000).
    """
    pattern = r'severity="E"' if jenkins else r'(E\d\d\d)'
    error = re.compile(pattern)
    return error.search(output)


def code_analysis_jshint(options):
    sys.stdout.write('JSHint')
    sys.stdout.flush()
    jenkins = _normalize_boolean(options['jenkins'])

    # cmd is a sequence of program arguments
    # first argument is child program
    paths = options['directory'].split('\n')
    cmd = [
        options['jshint-bin'],
        '--verbose',
        '--exclude={0}'.format(options['jshint-exclude'] or ' ')] + paths
    # Jenkins needs a specific format.
    if jenkins:
        cmd.append('--reporter=jshint')
    try:
        process = subprocess.Popen(
            cmd,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )
    except OSError:
        print('                 [\033[00;31m SKIP \033[0m]')
        return False
    output, err = process.communicate()
    if jenkins:
        log_filename = os.path.join(options['location'], 'jshint.xml')
        with open(log_filename, 'w') as jshint_log:
            jshint_log.write(output)
    # HACK: workaround for JSHint limitations
    if jshint_errors(output, jenkins):
        print('           [\033[00;31m FAILURE \033[0m]')
        # Name the pattern to use it in the substitution.
        old, new = '\((?P<name>E\d\d\d)\)', u'(\033[00;31m\g<name>\033[0m)'
        print _process_output(output, old, new)
        return False
    else:
        print('                [\033[00;32m OK \033[0m]')
        if output != '':
            print(output)  # XXX: there should be warnings on the output
        return True
