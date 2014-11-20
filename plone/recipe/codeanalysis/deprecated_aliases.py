# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log

import sys


def code_analysis_deprecated_aliases(options):
    log('title', 'Deprecated aliases')

    # XXX: advice on usage of the right option
    if options.get('deprecated-methods', 'False') != 'False':
        sys.stdout.write('\ndeprecated-methods option is deprecated; '
                         'use deprecated-aliases instead.')
    if options.get('deprecated-alias', 'False') != 'False':
        sys.stdout.write('\ndeprecated-alias option is deprecated; '
                         'use deprecated-aliases instead.')

    files = find_files(options, '.*\.py')
    if not files:
        log('ok')
        return True

    total_errors = []
    file_paths = files.strip().split('\n')
    for file_path in file_paths:
        with open(file_path, 'r') as file_handler:
            errors = _code_analysis_deprecated_aliases_lines_parser(
                file_handler.readlines(), file_path)

        if len(errors) > 0:
            total_errors += errors

    if len(total_errors) > 0:
        log('failure')
        for err in total_errors:
            print(err)
        return False
    else:
        log('ok')
        return True


def _code_analysis_deprecated_aliases_lines_parser(lines, file_path):
    errors = []
    linenumber = 0

    # Keep adding deprecated aliases and its newer counterparts as:
    # NEWER_VERSION : (LIST OF OLD METHODS)
    deprecated_aliases = {
        'assertEqual': ('failUnlessEqual', 'assertEquals', ),  # noqa
        'assertNotEqual': ('failIfEqual', ),  # noqa
        'assertTrue': ('failUnless', 'assert_', ),  # noqa
        'assertFalse': ('failIf', ),  # noqa
        'assertRaises': ('failUnlessRaises', ),  # noqa
        'assertAlmostEqual': ('failUnlessAlmostEqual', ),  # noqa
        'assertNotAlmostEqual': ('failIfAlmostEqual', ),  # noqa
    }

    msg = '{0}:{1}: found {2} replace it with {3}'

    for line in lines:
        linenumber += 1

        # allow to skip some methods if the comment # noqa is found
        if line.find('# noqa') != -1:
            continue

        try:
            deprecated_aliases_iteritems = deprecated_aliases.iteritems()
        except AttributeError:
            deprecated_aliases_iteritems = deprecated_aliases.items()  # PY3
        for newer_version, old_alias in deprecated_aliases_iteritems:
            for alias in old_alias:
                if line.find(alias) != -1:
                    errors.append(msg.format(
                        file_path,
                        linenumber,
                        alias,
                        newer_version)
                    )
                    continue

    return errors
