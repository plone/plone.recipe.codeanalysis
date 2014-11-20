# -*- coding: utf-8 -*-
import re
import subprocess
import sys

MAX_LINE_LENGTH = 20


def log(log_type, msg=None):
    if log_type == 'title':
        if msg:
            sys.stdout.write(msg)
        for i in range(0, MAX_LINE_LENGTH - len(msg)):
            sys.stdout.write(' ')
        sys.stdout.flush()
    elif log_type == 'ok':
        print('     [\033[00;32m OK \033[0m]')
    elif log_type == 'skip':
        print('   [\033[00;31m SKIP \033[0m]')
    elif log_type in ('failure', 'warning'):
        print('[\033[00;31m {0} \033[0m]'.format(log_type))
        if msg:
            print(msg)


def normalize_boolean(value):
    """Convert a string into a Boolean value.

    :param value: the string to be converted
    """
    return value.lower() == 'true'


def find_files(options, regex):
    paths = options['directory'].split('\n')
    cmd = ['find', '-L'] + paths + ['-regex', regex, '-type', 'f']
    process_files = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    files, err = process_files.communicate()
    if isinstance(files, bytes):
        return files.decode('utf-8')
    else:
        return files


def read_subprocess_output(cmd, output_file):
    """Run cmd and read the output from output_file.

    :param cmd: list containing command and options.
    :param output_file: file that will store the command output.
    :return: command output read from output_file.
    """
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=output_file
    )
    process.wait()
    output_file.flush()
    output_file.seek(0)
    output = output_file.read()
    return output, process.returncode


def process_output(output, old, new):
    """Replace all occurrences of substring 'old' with 'new' in 'output'.

    :param output: string containing command output
    :param old: substring to be found
    :param new: replace substring
    :return: string containing processed command output
    """
    error = re.compile(old)
    output = map(lambda x: error.sub(new, x), output.splitlines())
    return u'\n'.join(output)
