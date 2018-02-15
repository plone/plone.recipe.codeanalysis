# -*- coding: utf-8 -*-
from lxml.etree import parse
from lxml.etree import XMLSyntaxError
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory

import io
import re


# inspired by p01.checker:
#   http://pydoc.net/Python/p01.checker/0.5.6/p01.checker.checker/

DOCTYPE_WRAPPER = '''\
<!DOCTYPE html [<!ENTITY nbsp 'no-break space'>]>
{}'''


class ChameleonLint(Analyser):

    name = 'chameleon-lint'
    title = 'Chameleon Lint'
    extensions = ('pt', 'cpt')

    def cmd(self):
        # Please the ABC by faux-implementing the cmd.
        pass

    def run(self):
        files = []
        for extension in self.extensions:
            files.extend(self.find_files('.*\.{0}'.format(extension)))

        total_errors = []
        for file_path in files:
            file_content = open(file_path, 'r').read()
            offset = 0
            if '<!DOCTYPE' not in file_content:
                file_content = DOCTYPE_WRAPPER.format(file_content)
                offset = len(DOCTYPE_WRAPPER.splitlines()) - 1
            try:
                parse(io.StringIO(file_content))
            except XMLSyntaxError as e:
                # Line number offset correction.
                msg = e.msg
                for line_number in re.findall('line ([0-9]+)', msg):
                    msg = msg.replace(
                        'line {}'.format(line_number),
                        'line {}'.format(int(line_number) - offset))

                total_errors.append('{}: {}'.format(file_path, msg))

        with self.open_output_file() as output_file:
            output_file.write('\n'.join(total_errors))
            return self.parse_output(output_file, bool(total_errors))


def console_script(options):
    console_factory(ChameleonLint, options)
