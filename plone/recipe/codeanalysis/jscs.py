# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory
import re


class JSCS(Analyser):

    name = 'jscs'
    title = 'JSCS'
    output_file_extension = 'xml'

    @property
    def cmd(self):
        cmd = []
        files = self.find_files('.*\.js')

        if files:
            cmd.append(self.get_prefixed_option('bin'))

            if self.use_jenkins:
                cmd.append('--reporter=checkstyle')

            cmd.extend(files)

        return cmd

    def parse_output(self, output_file, return_code):
        """JSCS shows errors only, 2 different output types could occurr:
        - 1 code style error found.
        - No code style error found."""

        if self.use_jenkins:
            pattern = r'severity="error"'
        else:
            pattern = r'[0-9]+ code style errors? found\.'

        # skip warnings
        if not re.compile(pattern).search(output_file.read()):
            return_code = 0

        return super(JSCS, self).parse_output(output_file, return_code)


def console_script(options):
    console_factory(JSCS, options)
