# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory

import os


class Isort(Analyser):

    name = 'isort'
    title = 'Sort imports'
    output_file_extension = 'log'
    no_options = set(['isort-exclude', ])
    default_options = {
        'check-only': True,
        'diff': True,
        'force-alphabetical-sort': True,
        'force_single_line_imports': True,
        'length_sort': True,
        'line-width': '79',
        'multi_line': '3',
        'quiet': True,
    }

    @property
    def boolean_options(self):
        return set([
            key for key, value in self.default_options.items()
            if isinstance(value, bool)
        ])

    def get_isort_options(self):

        options = {}

        def option_parser(key, value):
            if key in self.boolean_options:
                if self.normalize_boolean(value) or \
                   (isinstance(value, bool) and value):
                    return '--{0}'.format(key)
            else:
                return '--{0}={1}'.format(key, value)

        for name, value in self.default_options.items():
            options[name] = option_parser(name, value)

        for option, value in self.options.items():
            if option in self.no_options or not option.startswith('isort-'):
                continue
            name = option.replace('isort-', '')
            options[name] = option_parser(name, value)

        return filter(None, options.values())  # omit None entries

    @property
    def cmd(self):
        cmd = []
        files = self.find_files('.*\.py')
        if files:
            cmd.append(os.path.join(self.options['bin-directory'], 'isort'))
            cmd.extend(self.get_isort_options())
            cmd.extend(files)

        return cmd


def console_script(options):
    console_factory(Isort, options)
