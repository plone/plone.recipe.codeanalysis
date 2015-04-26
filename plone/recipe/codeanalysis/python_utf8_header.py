# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines
import re


class UTF8Headers(CleanLines):

    name = 'utf8-header'
    title = 'Check utf-8 headers'
    message = '{0:s}: missing utf-8 header'
    checks = [
        {
            'extensions': ('py', ),
            'succeed': r'^#\s-\*-\scoding:\sutf-8\s-\*-$',
        },
    ]

    @staticmethod
    def validate_line(pattern, line):
        return re.compile(pattern).match(line)

    def check(self, file_path, succeed, **kwargs):
        with open(file_path, 'r') as file_handle:

            # Just check the first line of each file
            line = file_handle.readline()
            if UTF8Headers.validate_line(succeed, line):
                return []

        return [self.message.format(file_path), ]


def console_script(options):
    console_factory(UTF8Headers, options)
