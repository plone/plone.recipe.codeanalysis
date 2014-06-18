# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log
from plone.recipe.codeanalysis.utils import normalize_boolean
from plone.recipe.codeanalysis.utils import read_subprocess_output
from tempfile import TemporaryFile
import os
import re


def jscs_errors(output, jenkins=False):
    """Search for error on the output.

    JSCS shows errors only, 2 different output types could occurr:
    - 1 code style error found.
    - No code style error found.

    :param output: Output to be checked.
    :param jenkins: It is true when the jenkins output is turned on.

    """
    pattern = r'severity="error"' if jenkins else \
              r'[0-9]+ code style errors? found\.'
    error = re.compile(pattern)
    return error.search(output)


class CmdError(Exception):
    pass


def run_cmd(options, jenkins):
    """Run the jscs command using options.

    Run the jscs command using options and return the output.

    :param options: Options received by the code_analysis_jscs funciton.
    :param jenkins: It is true when the jenkins output is turned on.

    """
    # cmd is a sequence of program arguments
    cmd = [options['jscs-bin']]     # , '--reporter=inline', '--no-colors']

    all_files = find_files(options, '.*\.js').strip().split('\n')
    exc_files = find_files({
        'directory': options['jscs-exclude'],
    }, '.*\.js').strip().split('\n')

    # Remove excluded files
    files = set(all_files) - set(exc_files)

    if not files:
        log('ok')
        return ''

    # put all files in a single line
    cmd += list(files)

    try:
        if jenkins:
            cmd.append('--reporter=checkstyle')
            output_file_name = os.path.join(options['location'], 'jscs.xml')
            output_file = open(output_file_name, 'w+')
        else:
            output_file = TemporaryFile('w+')

        # Wrapper to subprocess.Popen
        try:
            # Return code is not used for jscs.
            output = read_subprocess_output(cmd, output_file)[0]
            return output
        except OSError:
            log('skip')
            message = 'Command: {0}. Outputfile: {1}'.format(cmd, output_file)
            raise CmdError(message)
    finally:
        output_file.close()


def code_analysis_jscs(options):
    log('title', 'JSCS')
    jenkins = normalize_boolean(options['jenkins'])

    try:
        output = run_cmd(options, jenkins)
    except CmdError:
        log('skip')
        return False

    if jscs_errors(output, jenkins):
        if jenkins:
            output_file_name = os.path.join(options['location'], 'jscs.xml')
            log('failure', 'Output file written to %s.' % output_file_name)
        else:
            log('failure', output)
        return False
    else:
        log('ok')
        return True
