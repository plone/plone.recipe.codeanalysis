# -*- coding: utf-8 -*-
import sys
import subprocess


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
    if process.returncode:
        print("          [\033[00;31m FAILURE \033[0m]")
        print(output)
        return False
    else:
        print("               [\033[00;32m OK \033[0m]")
        return True
