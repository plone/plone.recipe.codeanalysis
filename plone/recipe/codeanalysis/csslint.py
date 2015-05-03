# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory
import re


class CSSLint(Analyser):

    name = 'csslint'
    title = 'CSS Lint'
    output_file_extension = 'xml'
    output_regex = r'(?P<name>Error[^ -]*)'
    output_replace = '\033[00;31m\g<name>\033[0m'

    @property
    def cmd(self):
        cmd = []
        files = self.find_files('.*\.css')
        if files:
            cmd.append(self.get_prefixed_option('bin'))
            if self.use_jenkins:
                cmd.append('--format=lint-xml')
            cmd.extend(files)
        return cmd

    def parse_output(self, output_file, return_code):
        """Search for error markers as CSS Lint always return an exit code of 0
        either if a file has errors or just warnings.
        """
        if self.use_jenkins:
            pattern = r'severity="error"'
        else:
            pattern = r'Error -|error at'

        # skip warnings
        if not re.compile(pattern).search(output_file.read()):
            return_code = 0

        return super(CSSLint, self).parse_output(output_file, return_code)


def console_script(options):
    console_factory(CSSLint, options)
