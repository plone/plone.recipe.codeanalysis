# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.analyser import Analyser
from plone.recipe.codeanalysis.analyser import console_factory
import os
import subprocess


class CheckManifest(Analyser):

    name = 'check-manifest'
    title = 'Check MANIFEST.in'
    output_regex = r'(?P<name>Error[^ -]*)'
    output_replace = '\033[00;31m\g<name>\033[0m'

    @property
    def cmd(self):
        return [
            os.path.join(self.options['bin-directory'], 'check-manifest'),
            '-v'
        ]

    @property
    def packages(self):
        paths = set()
        items = CheckManifest.split_lines(
            self.options['check-manifest-directory'])
        for item in items:
            paths.add(os.path.realpath(item))
        if not paths:
            paths.add('.')
        return paths

    def run(self):
        output_file = self.open_output_file()
        status = True
        try:
            for package in self.packages:
                cmd = self.cmd
                cmd.append(package)
                try:
                    process = subprocess.Popen(cmd,
                                               stderr=subprocess.STDOUT,
                                               stdout=output_file)
                    process.wait()
                    output_file.flush()
                    output_file.seek(0)
                    status = status and self.parse_output(
                        output_file, process.returncode)
                except OSError:
                    self.log('skip')
        finally:
            output_file.close()
            return status


def console_script(options):
    console_factory(CheckManifest, options)
