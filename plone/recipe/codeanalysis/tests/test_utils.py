#!/usr/bin/env python
# -*- utf-8 -*-

import unittest
from plone.recipe.codeanalysis.utils import _process_output

class TestUtils(unittest.TestCase):
    def test_process_output_csslint_should_be_colored(self):
        original = ' x Error - x \n'
        expected = ' x \033[00;31mError\033[0m - x '
        old, new = 'Error -', '\033[00;31mError\033[0m -'
        output = _process_output(original, old, new)
        self.assertEqual(expected, output)

    def test_process_output_jshint_should_be_colored(self):
        original = ' x (E000) x \n'
        expected = ' x (\033[00;31mE000\033[0m) x '
        old, new = r'(E\d\d\d)', '(\033[00;31mE000\033[0m)'
        output = _process_output(original, old, new)

    def test_process_output_csslint_should_not_be_colored(self):
        original = ' x error - x '
        expected = ' x error - x '
        old, new = 'Error -', '\033[00;31mError\033[0m -'
        output = _process_output(original, old, new)

    def test_process_output_jshint_should_not_be_colored(self):
        original = ' x (E12A) x \nx E123 x'
        expected = ' x (E12A) x x E123 x'
        old, new = r'(E\d\d\d)', '(\033[00;31mE000\033[0m)'
        output = _process_output(original, old, new)