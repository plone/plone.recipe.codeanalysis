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

    @property
    def cmd(self):
        cmd = [
            os.path.join(self.options['bin-directory']) + '/flake8',
            '--ignore={0}'.format(self.get_prefixed_option('ignore')),
            '--exclude={0}'.format(self.get_prefixed_option('exclude')),
            '--max-complexity={0}'.format(
                self.get_prefixed_option('max-complexity')),
            '--max-line-length={0}'.format(
                self.get_prefixed_option('max-line-length'))
        ]

        paths_to_check = Flake8.split_lines(self.options['directory'])
        cmd.extend(paths_to_check)
        return cmd

    def open_output_file(self):
        if not self.filesystem:
            return super(Flake8, self).open_output_file()

        return open(os.path.join(self.options['location'], 'flake8.txt'), 'w+')


def console_script(options):
    console_factory(Flake8, options)
