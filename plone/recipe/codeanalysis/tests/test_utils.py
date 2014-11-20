# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import process_output
from plone.recipe.codeanalysis.utils import read_subprocess_output
from tempfile import NamedTemporaryFile
from tempfile import TemporaryFile
from tempfile import mkdtemp
import unittest


class TestUtils(unittest.TestCase):

    def test_process_output_csslint_should_be_colored(self):
        original = ' x Error - x '
        expected = u' x \033[00;31mError\033[0m - x '
        old, new = '(?P<name>Error[^ -]*)', u'\033[00;31m\g<name>\033[0m'
        output = process_output(original, old, new)
        self.assertEqual(expected, output)

    def test_process_output_jshint_should_be_colored(self):
        original = ' x (E000) x '
        expected = u' x (\033[00;31mE000\033[0m) x '
        old, new = '\((?P<name>E\d\d\d)\)', u'(\033[00;31m\g<name>\033[0m)'
        output = process_output(original, old, new)
        self.assertEqual(expected, output)

    def test_process_output_should_not_be_colored(self):
        original = ' x error - x '
        expected = u' x error - x '
        old, new = '(?P<name>Error[^ -]*)', u'\033[00;31m\g<name>\033[0m'
        output = process_output(original, old, new)
        self.assertEqual(expected, output)

        original = ' x (E12A) x x E123 x'
        expected = u' x (E12A) x x E123 x'
        old, new = '\((?P<name>E\d\d\d)\)', u'(\033[00;31m\g<name>\033[0m)'
        output = process_output(original, old, new)
        self.assertEqual(expected, output)

    def test_read_subprocess_output(self):
        output_file = TemporaryFile('w+')
        cmd = ['ls', '/']
        output, return_code = read_subprocess_output(cmd, output_file)
        output_file.close()
        self.assertTrue('tmp' in output, '{} not in {}'.format('tmp', output))
        self.assertEqual(0, return_code)

    def test_read_subprocess_should_raise_oserror(self):
        try:
            output_file = TemporaryFile('w+')
            cmd = ['fake_program', '/']
            self.assertRaises(
                OSError,
                read_subprocess_output,
                cmd, output_file)
        finally:
            output_file.close()

    def test_find_files(self):
        test_dir = mkdtemp()
        temp_files = []
        for n in range(1, 5):
            temp_file = NamedTemporaryFile(
                'w+',
                suffix='.py',
                prefix='tmp' + str(n),
                dir=test_dir)
            temp_files.append(temp_file)
        output = find_files({'directory': test_dir}, '.*py')
        sorted_output = '\n'.join(sorted(output.splitlines()))
        expect = '\n'.join([x.name for x in temp_files])
        self.assertEqual(expect, sorted_output)

    def test_find_files_not_dirs(self):
        test_dir = mkdtemp()
        temp_files = []
        for n in range(1, 5):
            temp_file = NamedTemporaryFile(
                'w+',
                suffix='.py',
                prefix='tmp' + str(n),
                dir=test_dir)
            temp_files.append(temp_file)
        mkdtemp(suffix='.py', dir=test_dir)
        output = find_files({'directory': test_dir}, '.*py')
        sorted_output = '\n'.join(sorted(output.splitlines()))
        expect = '\n'.join([x.name for x in temp_files])
        self.assertEqual(expect, sorted_output)
