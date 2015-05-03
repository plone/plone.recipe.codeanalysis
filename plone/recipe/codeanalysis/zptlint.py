# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class ZPTLint(Analyser):

    name = 'zptlint'
    title = 'ZPT Lint'
    output_file_extension = 'log'
    extensions = ('pt', 'cpt', 'zpt', )

    @property
    def cmd(self):
        cmd = []
        files = []
        for extension in self.extensions:
            files.extend(self.find_files('.*\.{0}'.format(extension)))

        if files:
            cmd.append(self.get_prefixed_option('bin'))
            cmd.extend(files)

        return cmd

    def parse_output(self, output_file, return_code):
        output_file.seek(0)

        if output_file.read() != '':
            # zptlint does not have a correct return_code
            return_code = 1

        return super(ZPTLint, self).parse_output(output_file, return_code)


def console_script(options):
    console_factory(ZPTLint, options)
