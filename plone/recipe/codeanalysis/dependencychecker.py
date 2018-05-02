# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class DependencyChecker(Analyser):

    name = 'dependencychecker'
    title = 'Check dependencies'

    @property
    def cmd(self):
        cmd = [self.get_prefixed_option('bin') or '']
        return cmd

    def parse_output(self, output_file, return_code):
        """dependencychecker always returns 0 even when
        errors are found. Catch that here.
        """
        has_errors = bool(output_file.read())
        output_file.seek(0)  # reset even though super does so as well
        return super(DependencyChecker, self).parse_output(
            output_file, has_errors)


def console_script(options):
    console_factory(DependencyChecker, options)
