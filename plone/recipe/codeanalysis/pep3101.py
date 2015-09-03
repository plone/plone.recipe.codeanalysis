# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines
import re

FAIL_RE = re.compile(r'^(?:[^\'"]*[\'"][^\'"]*[\'"])*\s*%|^\s*%')


class PEP3101(CleanLines):
    """
    Checking for old style formatting is hard in the real world.
    The logging module does not support PEP3101 yet, but then again,
    you are not supposed to give the formatted string but the
    format string and the parameters to be inserted.
    I knewer found a reference for that but know that sentry
    relies on it.
    So now this check, looks for:
    1: two string delimiter charactors following any number of whitespace and %
    2. Beginning of line, any number of whitespace and %

    This will ignore log messages that do not do inline message formatting,
    and it will find multiline old style log formatting.

    It will create false positives if you use % as a modulo operator
    and calculation spans multiple lines with the modulo character beginning
    a new line.
    """

    name = 'pep3101'
    title = 'PEP 3101'
    checks = [
        {
            'extensions': ('py', ),
            'fail': {
                FAIL_RE: '{0:s} formatter',
            },
        },
    ]


def console_script(options):
    console_factory(PEP3101, options)
