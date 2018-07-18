# -*- coding: utf-8 -*-
from lxml.etree import parse
from lxml.etree import XMLSyntaxError
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory

import io
import re
import sys


PY3 = sys.version_info > (3,)
if PY3:
    unicode = str

# inspired by p01.checker:
#   http://pydoc.net/Python/p01.checker/0.5.6/p01.checker.checker/

DOCTYPE_WRAPPER = """\
<!DOCTYPE html [<!ENTITY nbsp 'no-break space'>
                <!ENTITY times 'multiplication sign'>]>
{0}"""


class ChameleonLint(Analyser):

    name = 'chameleon-lint'
    title = 'Chameleon Lint'
    extensions = ('pt', 'cpt', 'zpt')

    def cmd(self):
        # Please the ABC by faux-implementing the cmd.
        pass

    def get_files(self):
        files = []
        for extension in self.extensions:
            files.extend(self.find_files('.*\.{0}'.format(extension)))
        return files

    def lint(self, file_content, file_path):
        offset = 0
        if '<!DOCTYPE' not in file_content:
            file_content = DOCTYPE_WRAPPER.format(file_content)
            offset = len(DOCTYPE_WRAPPER.splitlines()) - 1
        try:
            parse(io.StringIO(unicode(file_content)))
        except XMLSyntaxError as e:
            # Line number offset correction.
            msg = e.msg
            for line_number in re.findall('line ([0-9]+)', msg):
                msg = msg.replace(
                    'line {0}'.format(line_number),
                    'line {0}'.format(int(line_number) - offset))
            return '{0}: {1}'.format(file_path, msg)
        return None

    def linter(self, files):
        total_errors = []
        for file_path in files:
            file_content = open(file_path, 'r').read()
            error = self.lint(file_content, file_path)
            if error is not None:
                total_errors.append(error)
        return total_errors

    def report(self, errors):
        with self.open_output_file() as output_file:
            output_file.write('\n'.join(errors))
            return self.parse_output(output_file, bool(errors))

    def run(self):
        files = self.get_files()
        errors = self.linter(files)
        return self.report(errors)


def console_script(options):
    console_factory(ChameleonLint, options)
