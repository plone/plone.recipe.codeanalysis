# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import log
from plone.recipe.codeanalysis.utils import normalize_boolean
from plone.recipe.codeanalysis.utils import process_output
from plone.recipe.codeanalysis.utils import read_subprocess_output
from tempfile import TemporaryFile
import os
import re


class CmdError(Exception):
    pass


def jshint_errors(output, jenkins=False):
    """Search for error on the output.

    Search for error markers as JSHint always return an exit code of 2
    either if a file has errors or warnings. This method search for markers
    of errors (E000).

    :param output: Output to be checked.
    :param jenkins: It is true when the jenkins output is turned on.

    """
    pattern = r'severity="E"' if jenkins else r'(E\d\d\d)'
    error = re.compile(pattern)
    return error.search(output)


def run_cmd(options, jenkins):
    """Run the jshint command using options.

    Run the jshint command using options and return the output.

    :param options: Options received by the code_analysis_jshint funciton.
    :param jenkins: It is true when the jenkins output is turned on.

    """
    # cmd is a sequence of program arguments
    # first argument is child program
    paths = options['directory'].split('\n')
    cmd = [
        options['jshint-bin'],
        '--verbose',
        '--exclude={0}'.format(options['jshint-exclude'] or ' ')] + paths
    try:
        if jenkins:
            cmd.append('--reporter=jslint')
            output_file_name = os.path.join(options['location'], 'jshint.xml')
            output_file = open(output_file_name, 'w+')
        else:
            output_file = TemporaryFile('w+')

        # Wrapper to subprocess.Popen
        try:
            # Return code is not used for jshint.
            output = read_subprocess_output(cmd, output_file)[0]
            return output
        except OSError:
            log('skip')
            message = 'Command: {0}. Outputfile: {1}'.format(cmd, output_file)
            raise CmdError(message)
    finally:
        output_file.close()


def code_analysis_jshint(options):
    log('title', 'JSHint')
    jenkins = normalize_boolean(options['jenkins'])

    try:
        output = run_cmd(options, jenkins)
    except CmdError:
        log('skip')
        return False

    # HACK: workaround for JSHint limitations
    if jshint_errors(output, jenkins):
        if jenkins:
            output_file_name = os.path.join(options['location'], 'jshint.xml')
            log('failure', 'Output file written to %s.' % output_file_name)
        else:
            # Name the pattern to use it in the substitution.
            old, new = '\((?P<name>E\d\d\d)\)', u'(\033[00;31m\g<name>\033[0m)'
            log('failure', process_output(output, old, new))
        return False
    else:
        log('ok')
        if output != '' and not jenkins:
            # XXX: there should be warnings on the output
            log('warning', output)
        return True
