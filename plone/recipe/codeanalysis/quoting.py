# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines


class PreferSingleQuotes(CleanLines):

    name = 'prefer-single-quotes'
    title = 'Double quotes'
    message = '{0:s}:{1:d}: found {2:d} double quotes'
    checks = [{'extensions': ('py', ), }]

    def check(self, file_path, **kwargs):
        errors = []
        multiline = False
        with open(file_path, 'r') as file_handle:

            for linenumber, line in enumerate(file_handle.readlines()):

                # if there is no double quote sign
                # there's nothing to do
                if line.find('"') == -1:
                    continue

                # if it's a comment line ignore it
                if line.strip().startswith('#'):
                    continue

                # if it's a multiline string, is
                # ok to have doublequotes
                if line.find('"""') != -1:
                    # don't get trapped on multiline
                    # strings that are on a single line
                    if line.count('"""') == 2:
                        continue
                    elif multiline:
                        multiline = False
                    else:
                        multiline = True
                    continue

                # until the multiline is finished
                # it doesn't matter if single or
                # double quotes are used
                if multiline:
                    continue

                # if in the same line are both single
                # and double quotes, ignore it
                if line.find('"') != -1 and \
                        line.find("'") != -1:
                    continue

                double_quotes_count = line.count('"')
                errors.append(self.message.format(
                    file_path,
                    1 + linenumber,
                    double_quotes_count, ))

            return errors


def console_script(options):
    console_factory(PreferSingleQuotes, options)
