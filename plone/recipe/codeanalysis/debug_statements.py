# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines


class DebugStatements(CleanLines):

    name = 'debug-statements'
    title = 'Debug statements'
    checks = [
        {
            'extensions': ('py', ),
            'fail': {
                r'print\s*[\("\'\[]': '{0}',
            },
        },
        {
            'extensions': ('js', ),
            'fail': {
                r'console\.log': '{0}',
            },
        },
    ]


def console_script(options):
    console_factory(DebugStatements, options)
