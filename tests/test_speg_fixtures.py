import os
from os import path as op

from simplepeg.speg import SPEG

FIXTURES_ROOT = op.join(op.dirname(__file__), 'speg_fixtures')


def test_speg():
    grammar_path = op.join(FIXTURES_ROOT, 'grammar')
    text_path = op.join(FIXTURES_ROOT, 'text')
    result_path = op.join(FIXTURES_ROOT, 'result')

    file_names = []
    for (_, _, filenames) in os.walk(grammar_path):
        file_names.extend(filenames)

    for file_name in file_names:
        gfn = op.join(grammar_path, file_name)
        tfn = op.join(text_path, file_name + '.txt')
        rfn = op.join(result_path, file_name + '.json')
        with open(gfn, 'r') as g_file, open(tfn, 'r') as t_file, open(rfn, 'r') as r_file:
            grammar_content = g_file.read()
            text_content = t_file.read()
            result_content = r_file.read()
            speg = SPEG()
            ast = speg.parse(grammar_content, text_content)
            assert ast.to_json() == result_content
