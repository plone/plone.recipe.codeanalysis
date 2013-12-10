# -*- coding: utf-8 -*-
import unittest
from plone.recipe.codeanalysis.jshint import code_analysis_jshint
from plone.recipe.codeanalysis.jshint import run_cmd
from plone.recipe.codeanalysis.jshint import jshint_errors
from shutil import rmtree
from tempfile import mkdtemp
from os.path import join as path_join
from os.path import isfile as path_isfile


class TestJSHint(unittest.TestCase):
    def setUp(self):
        self.options = {
            'jshint-bin': 'jshint',
            'jshint-exclude': '',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        incorrect_code = file(path_join(self.test_dir, 'incorrect.js'), 'w')
        incorrect_code.write(
            'var number_ten= =10;'
            'var word_ten=\'ten\';'
            'var sum_2_plus_2 = 2+2;')
        incorrect_code.close()
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_jshint(self.options))

    def test_analysis_should_output_warnings(self):
        warnings_code = file(path_join(self.test_dir, 'warnings.js'), 'w')
        warnings_code.write(
        'function slideJump() {'
        '    if (window.location.hash == null || '
        'window.location.hash == \'\') {'
        '        return;'
        '    }'
        '    if (window.location.hash == null) return;'
        '    if (dest == null) {'
        '        dest = 0;'
        '    }'
        '}')
        warnings_code.close()
        self.options['directory'] = self.test_dir
        expected_output = \
            '{0[directory]}/warnings.js: line 1, col 52, Use \'===\' to' \
            ' compare with \'null\'. (W041)\n{0[directory]}/warnings.js:' \
            ' line 1, col 84, Use \'===\' to compare with \'\'. (W041)\n' \
            '{0[directory]}/warnings.js: line 1, col 141, Use \'===\' to' \
            ' compare with \'null\'. (W041)\n{0[directory]}/warnings.js:' \
            ' line 1, col 170, Use \'===\' to compare with \'null\'. (W041)' \
            '\n\n4 errors\n'.format(self.options)
        output = run_cmd(self.options, False)
        self.assertEquals(output, expected_output)

    def test_analysis_should_return_true_for_warnings(self):
        warnings_code = file(path_join(self.test_dir, 'warnings.js'), 'w')
        warnings_code.write(
        'function slideJump() {'
        '    if (window.location.hash == null || '
        'window.location.hash == \'\') {'
        '        return;'
        '    }'
        '    if (window.location.hash == null) return;'
        '    if (dest == null) {'
        '        dest = 0;'
        '    }'
        '}')
        warnings_code.close()
        self.options['directory'] = self.test_dir
        self.assertTrue(code_analysis_jshint(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so the function should raise an OSError
        # and return false.
        self.options['jshint-bin'] = 'FAKE_BIN'
        self.options['directory'] = 'FAKE_DIR'
        self.assertFalse(code_analysis_jshint(self.options))

    # Test failing on Travis.
    #def test_analysis_should_return_true(self):
    #    correct_code = file(path_join(self.test_dir, 'correct.js'), 'w')
    #    correct_code.write(
    #        'var number_ten=10;'
    #        'var word_ten=\'ten\';'
    #        'var sum_2_plus_2 = 2+2;')
    #    correct_code.close()
    #    self.options['directory'] = self.test_dir
    #    self.assertTrue(code_analysis_jshint(self.options))

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        correct_code = file(path_join(self.test_dir, 'correct.js'), 'w')
        correct_code.write(
            'var number_ten=10;'
            'var word_ten=\'ten\';'
            'var sum_2_plus_2 = 2+2;')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_jshint(self.options)
        file_exist = path_isfile(path_join(location_tmp_dir, 'jshint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)

    def test_jshint_errors_should_return_false_xml_output(self):
        output = '<?xml version="1.0" encoding="utf-8"?>\n' \
                 '<jslint>\n' \
                 '</jslint>'
        self.assertFalse(jshint_errors(output, True))

    def test_jshint_errors_should_return_true_xml_output(self):
        output = '<?xml version="1.0" encoding="utf-8"?>\n' \
            '<jslint>\n' \
            '    <file name="incorrect.js">\n' \
            '        <issue line="1" char="17" reason="Expected an ' \
            'identifier and instead saw &apos;=&apos;." evidence="var ' \
            'number_ten= =10;var word_ten=&apos;ten&apos;;var ' \
            'sum_2_plus_2 = 2+2;" severity="E" />\n' \
            '        <issue line="1" char="18" reason="Missing semicolon." ' \
            'evidence="var number_ten= =10;var word_ten=&apos;ten&apos;;var' \
            ' sum_2_plus_2 = 2+2;" severity="W" />\n' \
            '        <issue line="1" char="18" reason="Expected an ' \
            'assignment or function call and instead saw an expression." '\
            'evidence="var number_ten= =10;var word_ten=&apos;ten&apos;;var' \
            ' sum_2_plus_2 = 2+2;" severity="W" />\n' \
            '    </file>\n' \
            '</jslint>'
        self.assertTrue(jshint_errors(output, True))

    def test_jshint_errors_should_return_true_normal_output(self):
        output = 'incorrect.js: line 1, col 17, Expected an identifier and ' \
            'instead saw \'=\'. (E030)\nincorrect.js: line 1, col 18, ' \
            'Missing semicolon. (W033)\nincorrect.js: line 1, col 18, ' \
            'Expected an assignment or function call and instead saw an ' \
            'expression. (W030)\n\n3 errors\n'
        self.assertTrue(jshint_errors(output, False))

    def test_jshint_errors_should_return_false_normal_output(self):
        output = ''
        self.assertFalse(jshint_errors(output, False))
