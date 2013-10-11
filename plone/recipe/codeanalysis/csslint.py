# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import _normalize_boolean
from utils import _process_output

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
    sys.stdout.write('CSS Lint')
    sys.stdout.flush()
    jenkins = _normalize_boolean(options['jenkins'])

    # cmd is a sequence of program arguments
    # first argument is child program
    paths = options['directory'].split('\n')
    cmd = [options['csslint-bin']] + paths

    try:
        if jenkins:
            cmd.insert(1, '--format=lint-xml')
            output_file_name = os.path.join(options['location'], 'csslint.xml')
            outputfile = open(output_file_name, 'w+')
        else:
            outputfile = TemporaryFile('w+')

        try:
            subprocess.Popen(
                cmd,
                stderr=subprocess.STDOUT,
                stdout=outputfile
            )
        except OSError:
            print('               [\033[00;31m SKIP \033[0m]')
            return False

        outputfile.flush()
        outputfile.seek(0)
        output = outputfile.read()
    finally:
        outputfile.close()

    if csslint_errors(output, jenkins):
        print('          [\033[00;31m FAILURE \033[0m]')
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
        print('               [\033[00;32m OK \033[0m]')
        return True
