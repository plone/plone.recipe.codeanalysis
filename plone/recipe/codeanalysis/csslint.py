# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _normalize_boolean
from utils import _process_output
from plone.recipe.codeanalysis.utils import log

import os
import re
import subprocess
import sys
from tempfile import TemporaryFile


def csslint_errors(output, jenkins=False):
    """Search for error markers as CSS Lint always return an exit code of 0
    either if a file has errors or just warnings.
    """
    pattern = r'severity="error"' if jenkins else r'Error -'
    error = re.compile(pattern)
    return error.search(output)


def csslint_quiet_workaround(output):
    """Filter output to show only errors as CSS Lint '--quiet' option is just
    not working.

    :param output: string containing command output
    :return: string containing the filtered output
    """
    output = filter(csslint_errors, output.splitlines())
    return u''.join(output)


def code_analysis_csslint(options):
    log('title', 'CSS Lint')
    jenkins = _normalize_boolean(options['jenkins'])

    # cmd is a sequence of program arguments
    # first argument is child program
    paths = options['directory'].split('\n')
    cmd = [options['csslint-bin']] + paths

    try:
        if jenkins:
            cmd.insert(1, '--format=lint-xml')
            output_file_name = os.path.join(options['location'], 'csslint.xml')
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

    if csslint_errors(output, jenkins):
        log('failure')
        # XXX: if we are generating an XML file for Jenkins consumption
        #      then we will have no output here because our workaround
        #      is going to filter the whole stuff; we need to think on
        #      what's the best way to solve this later
        output = csslint_quiet_workaround(output)
        # TODO: pass color to _process_output
        # Name the pattern to use it in the substitution.
        old, new = '(?P<name>Error[^ -]*)', '\033[00;31m\g<name>\033[0m'
        print _process_output(output, old, new)
        return False
    else:
        log('ok')
        return True
