# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines
import re


class HasAttr(CleanLines):

    name = 'hasattr'
    title = 'hasattr'
    message = '{0:s}:{1}: found {2:s}'
    checks = [
        {
            'extensions': ('py', ),
            'fail': {
                re.compile(r'(^|.*\s)hasattr\(.+\).*'): 'hasattr',
            },
        }
    ]


def console_script(options):
    console_factory(HasAttr, options)
