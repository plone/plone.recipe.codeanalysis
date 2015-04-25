# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser


class TSLint(Analyser):

    name = 'tslint'
    title = 'TS Lint'
    output_file_extension = 'json'

    @property
    def cmd(self):
        all_files = TSLint.split_lines(self.find_files('.*\.ts'))
        exc_files = []

        # Should we exclude some files?
        exclude = TSLint.split_lines(self.get_prefixed_option('exclude'))
        if exclude:
            exc_files = TSLint.split_lines(self.find_files('.*\.ts',  exclude))

        # Remove excluded files
        files = set(all_files) - set(exc_files)
        if not files:
            return []

        cmd = [self.get_prefixed_option('bin'), ]
        for f in files:
            cmd.extend(['--file', f])

        if self.use_jenkins:
            cmd.insert(1, '--format=json')

        return cmd


def console_script(options):
    return TSLint(options).run()
