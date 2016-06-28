from __future__ import print_function
from os import path as op

import pytest

from simplepeg import speg_parser as sp
from utils import read_file, collect_files

FIXTURES_ROOT = op.join(op.dirname(__file__), 'speg_grammar_fixtures')


@pytest.mark.parametrize(
    'grammar_file',
    collect_files(op.join(FIXTURES_ROOT, 'valid')))
def test_speg_parser_valid(grammar_file):
    content = read_file(grammar_file)
    speg = sp.SimplePegParser()
    ast = speg.parse(content)
    last_error = speg.get_last_error()
    if last_error:
        print(last_error)
    assert ast


@pytest.mark.parametrize(
    'grammar_file',
    collect_files(op.join(FIXTURES_ROOT, 'invalid')))
def test_speg_parser_invalid(grammar_file):
    content = read_file(grammar_file)
    speg = sp.SimplePegParser()
    ast = speg.parse(content)
    assert not ast
