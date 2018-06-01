# -*- coding: utf-8 -*-
from lxml.etree import parse
from lxml.etree import XMLSyntaxError
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
        for file_path in files:
            try:
                parse(file_path)
            except XMLSyntaxError as e:
                total_errors.append('{0}: {1}'.format(file_path, e.msg))

        with self.open_output_file() as output_file:
            output_file.write('\n'.join(total_errors))
            return self.parse_output(output_file, bool(total_errors))


def console_script(options):
    console_factory(XMLLint, options)
