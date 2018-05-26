# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory


class I18NDude(Analyser):

    name = 'find-untranslated'
    title = 'Translations'
    extensions = ('pt', 'cpt', 'zpt')

    @property
    def cmd(self):
        cmd = []
        files = []
        for extension in self.extensions:
            files.extend(self.find_files('.*\.{0}'.format(extension)))

        if files:
            cmd.append(self.options.get('i18ndude-bin') or '')
            cmd.append('find-untranslated')
            if self.nosummary or self.use_jenkins:
                cmd.append('--nosummary')
            cmd.extend(files)

        return cmd

    @property
    def nosummary(self):
        """The report will contain only the errors for each file."""
        return I18NDude.normalize_boolean(
            self.get_prefixed_option('no-summary'),
        )


def console_script(options):
    console_factory(I18NDude, options)
