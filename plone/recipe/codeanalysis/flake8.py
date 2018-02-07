# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory

import os


class Flake8(Analyser):

    name = 'flake8'
    title = 'Flake8'
    output_file_extension = 'log'

    @property
    def filesystem(self):
        return Flake8.normalize_boolean(self.get_prefixed_option('filesystem'))

    def get_flake8_options(self):
        # plone.recipe.codeanalysis options that are not meant to be used
        # by flake8 itself or any of its plugins
        no_options = (
            'flake8-extensions',
            'flake8-filesystem',
        )
        # get the options
        options = [
            o for o in self.options
            if o.startswith('flake8-') and
            o not in no_options
        ]
        # format them
        options = [
            '{0}={1}'.format(
                o.replace('flake8', '-'),
                self.options.get(o),
            )
            for o in options
        ]
        if not self.normalize_boolean(self.options.get('multiprocessing')):
            options.append('--jobs=1')

        return options

    @property
    def cmd(self):
        cmd = [
            os.path.join(self.options['bin-directory'], 'flake8'),
        ]
        cmd.extend(self.get_flake8_options())

        paths_to_check = Flake8.split_lines(self.options['directory'])
        cmd.extend(paths_to_check)
        return cmd

    def open_output_file(self):
        if not self.filesystem:
            return super(Flake8, self).open_output_file()

        return open(os.path.join(self.options['location'], 'flake8.txt'), 'w+')


def console_script(options):
    console_factory(Flake8, options)
