# -*- coding: utf-8 -*-
import subprocess
import sys


def check(data):
    """Run p.r.codeanalysis when releasing with zest.releaser."""
    # import here to make zest.releaser a soft dependency
    from zest.releaser.utils import ask
    if not ask('Run code analysis before releasing?'):
        return

    try:
        subprocess.call(['bin/code-analysis'])
    except Exception as e:
        print(e)
        msg = 'Something went wrong when running "bin/code-analysis". ' \
              'Do you want to continue despite that?'
        if not ask(msg, default=False):
            sys.exit(1)
