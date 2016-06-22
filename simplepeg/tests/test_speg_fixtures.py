import os

from unittest import TestCase

from .. import speg as s


class TestSPEG(TestCase):
    def test_speg(self):
        self.maxDiff = None
        grammar_path = './simplepeg/tests/speg_fixtures/grammar/'
        text_path = './simplepeg/tests/speg_fixtures/text/'
        result_path = './simplepeg/tests/speg_fixtures/result/'
        file_names = []
        for (_, _, filenames) in os.walk(grammar_path):
            file_names.extend(filenames)
        for file_name in file_names:
            gfn = grammar_path + file_name
            tfn = text_path + file_name + '.txt'
            rfn = result_path + file_name + '.json'
            with open(gfn, 'r') as g_file, open(tfn, 'r') as t_file, open(rfn, 'r') as r_file:
                grammar_content = g_file.read()
                text_content = t_file.read()
                result_content = r_file.read()
                speg = s.SPEG()
                ast = speg.parse(grammar_content, text_content)
                ast_json_string = getattr(ast, 'to_json')()
                self.assertMultiLineEqual(ast_json_string, result_content)

