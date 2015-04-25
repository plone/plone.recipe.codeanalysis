# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser


class ZPTLint(Analyser):

    name = 'zptlint'
    title = 'ZPT Lint'
    output_file_extension = 'log'
    extensions = ('pt', 'cpt', 'zpt', )

    @property
    def cmd(self):
        cmd = []
        files = ''
        for extension in self.extensions:
            found_files = self.find_files('.*\.{0}'.format(extension))
            if found_files:
                files += found_files

        if files:
            cmd.append(self.get_prefixed_option('bin'))
            cmd.extend(files.split())

        return cmd


def console_script(options):
    return ZPTLint(options).run()
