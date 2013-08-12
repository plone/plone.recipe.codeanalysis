# -*- coding: utf-8 -*-
import re
import subprocess
import sys


def jshint_errors(output):
    """JSHint always return an exit code of 2 either if a file has errors or
    warnings. This method search for markers of errors (E000).
    """
    error = re.compile(r'(E\d\d\d)')
    return error.search(output)


def code_analysis_jshint(options):
    sys.stdout.write("JSHint")
    sys.stdout.flush()

    # cmd is a sequence of program arguments
    # first argument is child program
    cmd = [
        options['jshint-bin'],
        '--verbose',
        '--exclude={0}'.format(options['jshint-exclude'] or ' '),
        options['directory'],
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if jshint_errors(output):  # HACK: workaround for JSHint limitations
        print("           [\033[00;31m FAILURE \033[0m]")
        print(output)
    else:
        print("                [\033[00;32m OK \033[0m]")
        print(output)  # XXX: there should be warnings on the output
