# -*- coding: utf-8 -*-
import subprocess
import re


def _normalize_boolean(value):
    """Convert a string into a Boolean value.

    :param value: the string to be converted
    """
    return value.lower() == 'true'


def _find_files(options, regex):
    cmd = [
        'find',
        '-L',
        options['directory'],
        '-regex',
        regex
    ]
    process_files = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    files, err = process_files.communicate()
    return files


def _process_output(output, old, new):
    """Replace all ocurrences of substring 'old' with 'new' in 'output'.

    :param output: string containing command output
    :param old: substring to be found
    :param new: replace substring
    :return: string containing processed command output
    """
    error = re.compile(old)
    output = map(lambda x: error.sub(new, x), output.splitlines())
    return u'\n'.join(output)
