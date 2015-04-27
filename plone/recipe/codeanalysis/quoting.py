# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines
import re


class PreferSingleQuotes(CleanLines):

    name = 'prefer-single-quotes'
    title = 'Double quotes'
    message = '{0:s}:{1:d}: found double quotes'
    checks = [{'extensions': ('py', ), }]
    pattern = re.compile(r'\'\'\'|"""')

    def skip_line(self, line):
        if super(PreferSingleQuotes, self).skip_line(line):
            return True

        # if there is no double quote sign there's nothing to do
        if line.find('"') == -1:
            return True

        # if it's a comment line ignore it
        if re.compile(r'^\s*#').match(line):
            return True

    def wrapped_double_quotes(self, line):
        stack = []
        for char in line:
            if char in '"\'':
                if stack and stack[-1] == char:
                    stack.pop()
                    continue
                if not stack and char == '"':
                    return False

                stack.append(char)
            elif not stack and char == '#':
                # Supports line comment with double quotes
                stack.append(char)
        return True

    def check(self, file_path, **kwargs):
        stack = []
        errors = []
        with open(file_path, 'r') as file_handle:
            for linenumber, line in enumerate(file_handle.readlines()):

                # if it's a multiline string, is ok to have doublequotes
                multiline = self.pattern.findall(line)
                for quote in multiline:
                    if stack and quote == stack[-1]:
                        stack.pop()
                        continue

                    stack.append(quote)

                # until the multiline is finished it doesn't matter if single
                # or double quotes are used
                if stack or multiline:
                    continue

                if self.skip_line(line):
                    continue

                # if double quotes are in single, ignore it
                if self.wrapped_double_quotes(line):
                    continue

                errors.append(self.message.format(file_path, 1 + linenumber))

            return errors


def console_script(options):
    console_factory(PreferSingleQuotes, options)
