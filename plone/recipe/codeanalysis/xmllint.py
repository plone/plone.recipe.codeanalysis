# -*- coding: utf-8 -*-
import distutils
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class XMLLint(Analyser):

    name = 'xmllint'
    title = 'XML Lint'
    extensions = ('zcml', 'xsl', 'xml')

    @property
    def cmd(self):
        cmd = [distutils.spawn.find_executable('xmllint'), '--noout']

        files = []
        for extension in self.extensions:
            files.extend(self.find_files('.*\.{0}'.format(extension)))
        if files:
            cmd.extend(files)
        return cmd


def console_script(options):
    console_factory(XMLLint, options)
