# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory
import re


class JSHint(Analyser):

    name = 'jshint'
    title = 'JSHint'
    output_file_extension = 'xml'
    output_regex = r'\((?P<name>[EW]\d\d\d)\)'
    output_replace = '\033[00;31m\g<name>\033[0m'

    @property
    def cmd(self):
        cmd = []
        files = self.find_files('.*\.js')
        if files:
            cmd.extend([self.get_prefixed_option('bin'), '--verbose'])
            if self.use_jenkins:
                cmd.append('--reporter=jslint')
            cmd.extend(files)
        return cmd

    @property
    def suppress_warnings(self):
        return JSHint.normalize_boolean(
            self.get_prefixed_option('suppress-warnings'))

    def parse_output(self, output_file, return_code):
        """Search for error markers as JSHint always return an exit code of 2
        either if a file has errors or warnings. This method search for markers
        of errors (E000)."""

        # The behaviour was requested to be changed in #94, if this will
        # becoume our new default, we should mark this method as deprecated
        # and just removed it.
        if not self.suppress_warnings:
            return super(JSHint, self).parse_output(output_file, return_code)

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
