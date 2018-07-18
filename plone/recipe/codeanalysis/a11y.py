# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import console_factory
from plone.recipe.codeanalysis.chameleonlint import ChameleonLint

import sys


PY3 = sys.version_info > (3,)
if PY3:
    unicode = str


class A11yLint(ChameleonLint):

    name = 'a11y-lint'
    title = 'A1y (Accessibility) Lint'
    extensions = ('pt', 'cpt', 'zpt')

    def cmd(self):
        # Please the ABC by faux-implementing the cmd.
        pass

    def lint(self, file_content, file_path):
        error = super(A11yLint, self).lint(file_content, file_path)
        if error:
            return error
        pass  # do WASG here


def console_script(options):
    console_factory(A11yLint, options)
