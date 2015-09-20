# -*- coding: utf-8 -*-
import lxml.etree
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class XMLLint(Analyser):

    name = 'xmllint'
    title = 'XML Lint'
    extensions = ('zcml', 'xsl', 'xml')

    def cmd(self):
        # Please the ABC by faux-implementing the cmd.
        pass

    def run(self):
        files = []
        for extension in self.extensions:
            files.extend(self.find_files('.*\.{0}'.format(extension)))

        total_errors = []
        for file in files:
            try:
                lxml.etree.parse(file)
            except lxml.etree.XMLSyntaxError as e:
                total_errors.append('{}: {}'.format(file, e.message))

        if total_errors:
            self.log('failure', '\n'.join(total_errors))
            return False
        self.log('ok')
        return True


def console_script(options):
    console_factory(XMLLint, options)
