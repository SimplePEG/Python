from __future__ import print_function

import os
from os import path as op

from simplepeg import speg_parser as sp

FIXTURES_ROOT = op.join(op.dirname(__file__), 'speg_grammar_fixtures')


def test_speg_parser_valid():
    files_path = op.join(FIXTURES_ROOT, 'valid')

    file_names = []
    for (_, _, filenames) in os.walk(files_path):
        file_names.extend(filenames)

    for file_name in file_names:
        with open(op.join(files_path, file_name), 'r') as content_file:
            content = content_file.read()
            speg = sp.SimplePegParser()
            ast = speg.parse(content)
            last_error = speg.get_last_error()
        if last_error:
            print(last_error)
        assert ast


def test_speg_parser_invalid():
    files_path = op.join(FIXTURES_ROOT, 'invalid')
    file_names = []
    for (_, _, filenames) in os.walk(files_path):
        file_names.extend(filenames)

    for file_name in file_names:
        with open(op.join(files_path, file_name), 'r') as content_file:
            content = content_file.read()
            speg = sp.SimplePegParser()
            ast = speg.parse(content)
        assert not ast
