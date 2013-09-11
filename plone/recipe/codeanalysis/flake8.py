# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time


def code_analysis_flake8(options):
    sys.stdout.write("Flake8")
    sys.stdout.flush()

    # cmd is a sequence of program arguments
    # first argument is child program
    cmd = [
        os.path.join(options['bin-directory']) + '/flake8',
        '--ignore=%s' % options['flake8-ignore'],
        '--exclude=%s' % options['flake8-exclude'],
        '--max-complexity=%s' % options['flake8-max-complexity'],
        '--max-line-length=%s' % options['flake8-max-line-length'],
        options['directory'],
    ]
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    while process.poll() is None:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
    output, err = process.communicate()
    if options['jenkins']:
        flake8_log_filename = os.path.join(
            options['location'], "flake8.log")
        flake8_log = open(flake8_log_filename, "w")
        flake8_log.write(output)
        flake8_log.close()
    if process.returncode:
        print("          [\033[00;31m FAILURE \033[0m]")
        print(output)
        return False
    else:
        print("               [\033[00;32m OK \033[0m]")
        return True
