import pytest

from simplepeg.speg import SPEG
from simplepeg.exceptions import GrammarParseError, TextParseError


def test_grammar_parser_exception():
    speg = SPEG()
    with pytest.raises(GrammarParseError):
        speg.parse_grammar('!!!')


def test_text_parser_exception():
    speg = SPEG()
    speg.parse_grammar('GRAMMAR test a -> "A";')
    with pytest.raises(TextParseError):
        speg.parse_text('B')


def test_grammar_before_text():
    speg = SPEG()
    with pytest.raises(Exception):
        speg.parse_text('B')


def test_speg_parse_grammar_parser_exception():
    speg = SPEG()
    with pytest.raises(GrammarParseError):
        speg.parse('!!!', 'B')


def test_speg_parse_text_parser_exception():
    speg = SPEG()
    with pytest.raises(TextParseError):
        speg.parse('GRAMMAR test a -> "A";', 'B')
