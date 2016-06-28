from os import path as op
import json

import pytest

from simplepeg.speg import SPEG
from utils import collect_files, read_file

FIXTURES_ROOT = op.join(op.dirname(__file__), 'speg_fixtures')


@pytest.mark.parametrize(
    'grammar_file',
    collect_files(FIXTURES_ROOT, lambda f: f.endswith('.peg')))
def test_speg(grammar_file):
    grammar, text, result = [
        read_file(grammar_file + postfix)
        for postfix in ('', '.txt', '.json')]
    speg = SPEG()
    ast = speg.parse(grammar, text)
    assert json.loads(ast.to_json()) == json.loads(result)
