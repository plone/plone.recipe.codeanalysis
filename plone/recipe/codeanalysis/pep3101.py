# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines
import re


class PEP3101(CleanLines):

    name = 'pep3101'
    title = 'PEP 3101'
    checks = [
        {
            'extensions': ('py', ),
            'fail': {
                re.compile(r'%(?:\(\w+\))?(?:s|i|p|r)'): '{0:s} formatter',
            },
        },
    ]


def console_script(options):
    console_factory(PEP3101, options)
