import os

from unittest import TestCase

from .. import speg_parser as sp


class TestSPEGParser(TestCase):
    def test_speg_parser_valid(self):
        ast = False
        last_error = False
        files_path = './simplepeg/tests/speg_grammar_fixtures/valid/'
        file_names = []
        for (_, _, filenames) in os.walk(files_path):
            file_names.extend(filenames)
        for file_name in file_names:
            with open(files_path + file_name, 'r') as content_file:
                content = content_file.read()
                speg = sp.SPEG_parser()
                ast = speg.parse(content)
                last_error = speg.getLastError()
            if last_error:
                print last_error
            self.assertNotEqual(ast, False, 'Failed to parse ' + file_name)
    def test_speg_parser_invalid(self):
        ast = False
        files_path = './simplepeg/tests/speg_grammar_fixtures/invalid/'
        file_names = []
        for (_, _, filenames) in os.walk(files_path):
            file_names.extend(filenames)
        for file_name in file_names:
            with open(files_path + file_name, 'r') as content_file:
                content = content_file.read()
                speg = sp.SPEG_parser()
                ast = speg.parse(content)
            self.assertEqual(ast, False, 'Should fail to parse ' + file_name)