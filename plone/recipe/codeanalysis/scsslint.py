# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class SCSSLint(Analyser):

    name = 'scsslint'
    title = 'SCSS Lint'
    output_file_extension = 'xml'

    @property
    def cmd(self):
        cmd = []
        files = self.find_files('.*\.scss')

        if files:
            cmd.append(self.options.get('scsslint-bin'))
            config = self.options.get('scsslint-config')
            if config:
                cmd.extend(['--config', config])
            cmd.extend(files)

        return cmd


def console_script(options):
    console_factory(SCSSLint, options)