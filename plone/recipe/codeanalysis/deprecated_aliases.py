# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.clean_lines import CleanLines


class DeprecatedAliases(CleanLines):

    name = 'deprecated-aliases'
    title = 'Deprecated aliases'
    message = '{0:s}:{1:d}: found {2:s} replace it with {3:s}'
    checks = [
        {
            'extensions': ('py', ),
            'fail': {
                'assertEqual': ('failUnlessEqual', 'assertEquals', ),  # noqa
                'assertNotEqual': ('failIfEqual', ),  # noqa
                'assertTrue': ('failUnless(', 'assert_', ),  # noqa
                'assertFalse': ('failIf(', ),  # noqa
                'assertRaises': ('failUnlessRaises', ),  # noqa
                'assertAlmostEqual': ('failUnlessAlmostEqual', ),  # noqa
                'assertNotAlmostEqual': ('failIfAlmostEqual', ),  # noqa
            },
        },
    ]

    @staticmethod
    def validate_line(pattern, line):
        return line.find(pattern) != -1

    def check(self, file_path, fail={}, **kwargs):
        errors = []
        with open(file_path, 'r') as file_handle:
            for linenumber, line in enumerate(file_handle.readlines()):
                if self.skip_line(line):
                    continue
                for newer_version, old_alias in fail.items():
                    for alias in old_alias:
                        if DeprecatedAliases.validate_line(alias, line):
                            errors.append(self.message.format(
                                file_path,
                                1 + linenumber,
                                alias,
                                newer_version)
                            )
        return errors


def console_script(options):
    console_factory(DeprecatedAliases, options)
