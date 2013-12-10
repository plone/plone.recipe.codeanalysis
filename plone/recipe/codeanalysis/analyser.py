# -*- coding: utf-8 -*-
from tempfile import TemporaryFile
from utils import log
import os
import subprocess


class CmdError(Exception):
    pass


class Analyser():
    def __init__(
            self,
            jenkins_filename='analysis.xml',
            options=None,
            cmd_args=None):
        """Instance initializer.

        :param jenkins_filename: When running on jenkins, the output is
        written to a file using this name.
        :param options: Arguments can be passed to the analysers.
        :param cmd_args: Fixed arguments that are used to format the output.
        """
        if options is None:
            options = {'bin': 'echo'}
        if cmd_args is None:
            cmd_args = ['some_arg']

        self.options = options
        self.cmd_args = cmd_args
        self.jenkins_filename = jenkins_filename
        self.output_file = None
        self.output = ''
        self.return_code = None

    def normalize_boolean(self, value=None):
        """Convert a string into a Boolean value.

        :param value: the string to be converted
        """
        if value is None:
            value = ''
        return value.lower() == 'true'

    @property
    def jenkins_output_fullpath(self):
        """Fullpath of the jenkins output file name.

        If uses the location option to generate the full path of the jenkins
        output file name.

        :return: The full path of jenkins output filename using the given
        location option.
        """
        location = self.options.get('location', '')
        filename = self.jenkins_filename
        return os.path.join(location, filename)

    @property
    def use_jenkins(self):
        """Cast the jenkins option from string to boolean.

        :return: Jenkins option casted to boolean.
        """
        return self.normalize_boolean(self.options.get('jenkins'))

    @property
    def cmd(self):
        """Readonly property that join the analyser command and arguments.

        :return: List containing the command and arguments, to be used by
        the subprocess.Popen method.
        """
        paths = self.options.get('directory', '\n').split('\n')
        cmd = [self.options.get('bin')]
        cmd.extend(self.cmd_args)
        cmd.extend(paths)
        return cmd

    def open_output_file(self):
        """Open output file according to the jenkins option.

        If the analyser is running on jenkins a regular file is open,
        otherwise it open a temporary file. This file is used to store
        the analyser command output. The PIPE system, used by the
        subprocess module have a limitation, so a temporary file is used.
        """
        if self.use_jenkins:
            output_filename = self.jenkins_output_fullpath
            self.output_file = open(output_filename, 'w+')
        else:
            self.output_file = TemporaryFile('w+')

    def run(self):
        """Run the analyser command using options.

        Run the analyser command using options and return the output. The
        analyser command is defined by the 'bin' option, it can be any one
        of the external analyser commands, as csslint, jshint, flake8, for
        example. The return code is stored on the return_code attribute.
        The output is returned but is also stored in the output attribute.

        :return: It return the output of the analyser command.
        """
        try:
            self.open_output_file()
            try:
                self.output, self.return_code = self.read_subprocess_output()
                return self.output
            except OSError:
                log('skip')
                raise CmdError()
        finally:
            self.output_file.close()

    def read_subprocess_output(self):
        """Run cmd and read the output from output_file.

        :return: command output read from output_file.
        """
        process = subprocess.Popen(
            self.cmd,
            stderr=subprocess.STDOUT,
            stdout=self.output_file
        )
        process.wait()
        self.output_file.flush()
        self.output_file.seek(0)
        output = self.output_file.read()
        return output, process.returncode
