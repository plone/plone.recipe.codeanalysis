# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory
import re


class CleanLines(Analyser):

    name = 'clean-lines'
    title = 'Check clean lines'
    message = '{0:s}:{1:d}: found {2:s}'
    checks = [
        {
            'extensions': (
                'py', 'pt', 'zcml', 'xml',  # standard plone extensions
                'js', 'css', 'html',  # html stuff
                'rst', 'txt', 'md',  # documentation
            ),
            'fail': {
                r' $': 'trailing spaces',
                r'\t': 'tabs',
            },
        }
    ]
    ignore_patterns = (
        r'#\snoqa',
        r'//\snoqa',
    )

    def skip_line(self, line):
        for pattern in self.ignore_patterns:
            if re.compile(pattern).search(line):
                return True
        return False

    @staticmethod
    def validate_line(pattern, line):
        return re.compile(pattern).search(line)

    def check(self, file_path, fail={}, succeed={}, **kwargs):
        errors = []
        with open(file_path, 'r') as file_handle:
            for linenumber, line in enumerate(file_handle.readlines()):
                if self.skip_line(line):
                    continue

                # Fail if one of the fail items was found
                for check, message in fail.items():
                    match = CleanLines.validate_line(check, line)

                    if match:
                        message = message.format(match.group())
                        errors.append(self.message.format(
                            file_path, 1 + linenumber, message
                        ))

                # Fail if succeed was not found
                for check, message in succeed.items():
                    if CleanLines.validate_line(check, line):
                        continue

                    errors.append(self.message.format(
                        file_path, 1 + linenumber, message
                    ))

        return errors

    def cmd(self):
        pass

    def run(self):
        # Should we exclude some files?
        total_errors = []

        for check in self.checks:
            files = []
            for extension in check['extensions']:
                files.extend(self.find_files('.*\.{0}'.format(extension)))
            for file_path in files:
                total_errors.extend(self.check(file_path, **check))

        if total_errors:
            self.log('failure', '\n'.join(total_errors))
            return False

        self.log('ok')
        return True


def console_script(options):
    console_factory(CleanLines, options)
