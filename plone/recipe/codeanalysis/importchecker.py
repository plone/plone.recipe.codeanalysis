# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class ImportChecker(Analyser):

    name = 'importchecker'
    title = 'Check unused imports'
    extensions = ('py', )

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
        """importchecker always exits with code 0.
        Provide proper result status here.
        """
        if output_file.read():
            return_code = 1
        return super(ImportChecker, self).parse_output(
            output_file, return_code)


def console_script(options):
    console_factory(ImportChecker, options)
