# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory

import os


class SCSSLint(Analyser):

    name = 'scsslint'
    title = 'SCSS Lint'
    output_file_extension = 'xml'

    @property
    def cmd(self):
        linter = self.options.get('scsslint-bin')
        cmd = []
        files = self.find_files('.*\.scss')

        if (files or self.use_jenkins) and linter:
            cmd.append(linter)
            if self.use_jenkins:
                cmd.extend(['--require=scss_lint_reporter_checkstyle',
                            '--format=Checkstyle'])
                # Jenkins needs to always find a valid checkstyle xml
                # even in the absence of scss files. But scss-lint requires
                # files to check. So give it one.
                if files == [] and 'location' in self.options:
                    fakeit = os.path.join(self.options.get('location'),
                                          'fakeit.scss')
                    fh = open(fakeit, 'w+t')
                    fh.write('.foo { padding: 1px; }\n')
                    files.append(fakeit)
            config = self.options.get('scsslint-config')
            if config:
                cmd.extend(['--config', config])
            cmd.extend(files)

        return cmd

    def parse_output(self, output_file, return_code):
        """Strip anything, like ruby deprecation warnings, from the start of the file
        if we're in Jenkins mode (i.e. emitting xml)'
        """
        if self.use_jenkins:
            clean_output = []
            output_file.seek(0)
            for line in output_file.readlines():
                if clean_output or line.startswith('<?xml'):
                    clean_output.append(line)
            output_file.seek(0)
            output_file.truncate()  # or we'll have dangling "old" lines
            output_file.write('\n'.join(clean_output))
            output_file.seek(0)
        return super(SCSSLint, self).parse_output(output_file, return_code)


def console_script(options):
    console_factory(SCSSLint, options)
