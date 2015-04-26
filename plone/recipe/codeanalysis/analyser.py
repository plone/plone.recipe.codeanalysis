# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractproperty
from tempfile import TemporaryFile
from time import time
import os
import re
import subprocess
import sys


def is_string(unknown):
    if sys.version_info[0] < 3:
        return isinstance(unknown, basestring)  # noqa for python3
    return isinstance(unknown, str)


def console_factory(klass, options):
    if not klass(options).run():
        sys.exit(1)
    sys.exit(0)


class Analyser:

    __metaclass__ = ABCMeta

    output_file_extension = 'log'
    output_regex = r'(.*)'  # substring to be found
    output_replace = r'\1'  # replace substring

    colors = {
        'ok': '[\033[00;32m {0:s} \033[0m]',
    }

    def __init__(self, options, lock=None):
        """Instance initializer.

        :param options: Arguments can be passed to the analysers.
        """
        self.options = options
        self.lock = lock
        self.start = time()

    @abstractproperty
    def title(self):
        pass

    @abstractproperty
    def name(self):
        pass

    def log(self, log_type, msg=None):
        if self.lock:
            self.lock.acquire()

        out = self.colors.get(log_type, '[\033[00;31m {0:s} \033[0m]')
        print('{0:.<30}{1:.>25} in {2:.03f}s'.format(
            self.title,
            out.format(log_type.upper()),
            time() - self.start,
        ))

        if msg:
            print(msg)

        if self.lock:
            self.lock.release()

    @property
    def enabled(self):
        return self.normalize_boolean(self.options.get(self.name))

    @property
    def output_filename(self):
        return '{0:s}.{1:s}'.format(self.name, self.output_file_extension)

    @staticmethod
    def normalize_boolean(value):
        """Convert a string into a Boolean value.

        :param value: the string to be converted
        """
        if is_string(value) and value.strip():
            return value.lower() == 'true'
        return False

    @staticmethod
    def split_lines(value):
        """Convert a multiline string into a list of strings.

        :rtype : list
        :param value: the string to be converted
        """
        if is_string(value) and value.strip():
            return value.split('\n')
        return []

    def get_prefixed_option(self, option):
        return self.options.get('{0:s}-{1:s}'.format(self.name, option))

    @property
    def use_jenkins(self):
        """Cast the jenkins option from string to boolean.

        :return: Jenkins option casted to boolean.
        """
        return Analyser.normalize_boolean(self.options.get('jenkins'))

    @property
    def cmd(self):
        """Readonly property that join the analyser command and arguments.

        :rtype : list
        :return: List containing the command and arguments, to be used by
        the subprocess.Popen method.
        """
        paths = Analyser.split_lines(self.options.get('directory', ''))
        cmd = [self.options.get('bin')]
        cmd.extend(self.cmd_args)
        cmd.extend(paths)
        return cmd

    def find_files(self, regex, paths=None):
        if paths is None:
            paths = Analyser.split_lines(self.options['directory'])

        dirs = []
        files = []
        for path in paths:
            realpath = os.path.realpath(path)
            if os.path.isdir(realpath) and realpath not in dirs:
                dirs.append(realpath)
            if os.path.isfile(realpath) and realpath not in files:
                files.append(realpath)

        cmd = ['find', '-L'] + dirs + ['-regex', regex, '-type', 'f']
        process_files = subprocess.Popen(
            cmd,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )
        exclude, err = process_files.communicate()
        if isinstance(exclude, bytes):
            exclude = exclude.decode('utf-8')

        files.insert(0, exclude.strip())
        return '\n'.join(files)

    def open_output_file(self):
        """Open output file according to the jenkins option.

        If the analyser is running on jenkins a regular file is open,
        otherwise it open a temporary file. This file is used to store
        the analyser command output. The PIPE system, used by the
        subprocess module have a limitation, so a temporary file is used.
        """
        if not self.use_jenkins:
            return TemporaryFile('w+')

        return open(
            os.path.join(self.options['location'], self.output_filename), 'w+')

    def process_output(self, output):
        """Replace all occurrences of substring ``self.output_regex``
           with ``self.output_replace`` in ``output``.

        :param output: string containing command output
        :return: string containing processed command output
        """
        error = re.compile(self.output_regex)
        output = map(
            lambda x: error.sub(self.output_replace, x), output.splitlines()
        )
        return u'\n'.join(output).strip()

    def parse_output(self, output_file, return_code):
        if return_code:
            output_file.seek(0)

            if self.use_jenkins:
                self.log(
                    'failure',
                    'Output file written to {0}.'.format(output_file.name)
                )
            else:
                self.log(
                    'failure',
                    self.process_output(output_file.read())
                )
            return False
        else:
            self.log('ok')
            return True

    def run(self):
        """Run the analyser command using options.

        Run the analyser command using options and return the output. The
        analyser command is defined by the 'bin' option, it can be any one
        of the external analyser commands, as csslint, jshint, flake8, for
        example. The return code is stored on the return_code attribute.
        The output is returned but is also stored in the output attribute.

        :return: It return the output of the analyser command.
        """
        output_file = self.open_output_file()

        try:
            assert len(self.cmd) > 0  # skip if there's no command
            process = subprocess.Popen(self.cmd,
                                       stderr=subprocess.STDOUT,
                                       stdout=output_file)
            process.wait()
            output_file.flush()
            output_file.seek(0)
            return self.parse_output(output_file, process.returncode)
        except AssertionError:
            self.log('ok')
            return True
        except OSError:
            self.log('skip')
            return False
        finally:
            output_file.close()
