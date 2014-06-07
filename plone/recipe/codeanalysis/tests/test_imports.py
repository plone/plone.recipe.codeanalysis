# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.imports import code_analysis_imports
from shutil import rmtree
from tempfile import mkdtemp
import os
import unittest

VALID = """\
from Foo.bar import baz\n\
from foo.Bar import baz\n\
from foo.bar import Baz\n\
from foo.bar import baz\n\
import baz\n\
"""  # noqa

INVALID_SORTED = """\
from Foo.bar import baz\n\
from foo.bar import Baz\n\
from foo.Bar import baz\n\
from foo.bar import baz\n\
import baz\n\
"""  # noqa

INVALID_GROUPED = """\
from Foo import (bar, baz)\n\
from foo import Baz, baz\n\
"""  # noqa


class TestImports(unittest.TestCase):

    def setUp(self):
        self.options = {
            'imports': 'True',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def _create_file_in_test_dir(self, filename, contents):
        with open(os.path.join(self.test_dir, filename), 'w') as f:
            f.write(contents)
        self.options['directory'] = self.test_dir

    def test_analysis_should_return_false_on_grouped_imports(self):
        self._create_file_in_test_dir('invalid.py', INVALID_GROUPED)
        self.assertFalse(code_analysis_imports(self.options))

    def test_analysis_should_return_false_on_unsorted_imports(self):
        filename = 'invalid.py'
        self._create_file_in_test_dir(filename, INVALID_SORTED)
        self.assertFalse(code_analysis_imports(self.options))

    def test_analysis_should_return_true_for_valid_files(self):
        self._create_file_in_test_dir('valid.py', VALID)
        self.assertTrue(code_analysis_imports(self.options))
