# -*- coding: utf-8 -*-
import re
import subprocess
import sys


def csslint_errors(output):
    """CSS Lint always return an exit code of 0 either if a file has errors or
    warnings. This method search for markers of errors 'Error -'.
    """
    error = re.compile(r'Error -')
    return error.search(output)


def code_analysis_csslint(options):
    sys.stdout.write("CSS Lint")
    sys.stdout.flush()

    # cmd is a sequence of program arguments
    # first argument is child program
    cmd = [
        options['csslint-bin'],
        options['directory'],
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    output, err = process.communicate()
    if csslint_errors(output):  # HACK: workaround for CSS Lint limitations
        print("          [\033[00;31m FAILURE \033[0m]")
        print(output)
        return False
    else:
        print("               [\033[00;32m OK \033[0m]")
        if output != '':
            print(output)  # XXX: there should be warnings on the output
        return True
