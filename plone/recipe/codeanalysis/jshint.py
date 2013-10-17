# -*- coding: utf-8 -*-

from plone.recipe.codeanalysis.utils import _normalize_boolean
from plone.recipe.codeanalysis.utils import _process_output
from plone.recipe.codeanalysis.utils import log

import os
import re
import subprocess
from tempfile import TemporaryFile


def jshint_errors(output, jenkins=False):
    """Search for error markers as JSHint always return an exit code of 2
    either if a file has errors or warnings. This method search for markers
    of errors (E000).
    """
    pattern = r'severity="E"' if jenkins else r'(E\d\d\d)'
    error = re.compile(pattern)
    return error.search(output)


def code_analysis_jshint(options):
    log('title', 'JSHint')
    jenkins = _normalize_boolean(options['jenkins'])

    # cmd is a sequence of program arguments
    # first argument is child program
    paths = options['directory'].split('\n')
    cmd = [
        options['jshint-bin'],
        '--verbose',
        '--exclude={0}'.format(options['jshint-exclude'] or ' ')] + paths
    try:
        if jenkins:
            cmd.append('--reporter=jshint')
            output_file_name = os.path.join(options['location'], 'jshint.xml')
            output_file = open(output_file_name, 'w+')
        else:
            output_file = TemporaryFile('w+')

        try:
            subprocess.Popen(
                cmd,
                stderr=subprocess.STDOUT,
                stdout=output_file
            )
        except OSError:
            log('skip')
            return False

        output_file.flush()
        output_file.seek(0)
        output = output_file.read()
    finally:
        output_file.close()

    # HACK: workaround for JSHint limitations
    if jshint_errors(output, jenkins):
        log('failure')
        # Name the pattern to use it in the substitution.
        old, new = '\((?P<name>E\d\d\d)\)', u'(\033[00;31m\g<name>\033[0m)'
        print _process_output(output, old, new)
        return False
    else:
        log('ok')
        if output != '':
            print(output)  # XXX: there should be warnings on the output
        return True
