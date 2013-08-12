# -*- coding: utf-8 -*-
import subprocess


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
