# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class I18NDude(Analyser):

    name = 'find-untranslated'
    title = 'Translations'

    @property
    def cmd(self):
        cmd = []
        files = I18NDude.split_lines(self.find_files('.*\.pt'))

        if files:
            cmd.append(self.options.get('i18ndude-bin') or '')
            cmd.append('find-untranslated')
            cmd.extend(files)

        return cmd


def console_script(options):
    console_factory(I18NDude, options)
