# -*- utf-8 -*-

import unittest
from plone.recipe.codeanalysis.utils import _process_output


class TestUtils(unittest.TestCase):
    def test_process_output_csslint_should_be_colored(self):
        original = ' x Error - x '
        expected = u' x \033[00;31mError\033[0m - x '
        old, new = '(?P<name>Error[^ -]*)', u'\033[00;31m\g<name>\033[0m'
        output = _process_output(original, old, new)
        self.assertEqual(expected, output)

    def test_process_output_jshint_should_be_colored(self):
        original = ' x (E000) x '
        expected = u' x (\033[00;31mE000\033[0m) x '
        old, new = '\((?P<name>E\d\d\d)\)', u'(\033[00;31m\g<name>\033[0m)'
        output = _process_output(original, old, new)
        self.assertEqual(expected, output)

    def test_process_output_should_not_be_colored(self):
        original = ' x error - x '
        expected = u' x error - x '
        old, new = '(?P<name>Error[^ -]*)', u'\033[00;31m\g<name>\033[0m'
        output = _process_output(original, old, new)
        self.assertEqual(expected, output)

        original = ' x (E12A) x x E123 x'
        expected = u' x (E12A) x x E123 x'
        old, new = '\((?P<name>E\d\d\d)\)', u'(\033[00;31m\g<name>\033[0m)'
        output = _process_output(original, old, new)
        self.assertEqual(expected, output)
