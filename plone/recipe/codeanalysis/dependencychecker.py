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


def console_script(options):
    console_factory(DependencyChecker, options)
