# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory
import re


class JSHint(Analyser):

    name = 'jshint'
    title = 'JSHint'
    output_file_extension = 'xml'
    output_regex = r'\((?P<name>E\d\d\d)\)'
    output_replace = '\033[00;31m\g<name>\033[0m'

    @property
    def cmd(self):
        cmd = [self.get_prefixed_option('bin'), '--verbose']

        if self.use_jenkins:
            cmd.append('--reporter=jslint')

        excludes = JSHint.split_lines(self.get_prefixed_option('exclude'))
        if excludes:
            cmd.append('--exclude={0}'.format(','.join(excludes)))

        cmd.extend(JSHint.split_lines(self.options['directory']))
        return cmd

    def parse_output(self, output_file, return_code):
        """Search for error markers as JSHint always return an exit code of 2
        either if a file has errors or warnings. This method search for markers
        of errors (E000)."""

        if self.use_jenkins:
            pattern = r'severity="E"'
        else:
            pattern = r'(E\d\d\d)'

        output = output_file.read()
        if return_code != 0 and not re.compile(pattern).search(output):
            return_code = 0

        return super(JSHint, self).parse_output(output_file, return_code)


def console_script(options):
    console_factory(JSHint, options)
