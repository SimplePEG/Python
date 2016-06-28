from unittest import TestCase

from .. import speg as s


class TestSPEGExceptions(TestCase):
    def test_grammar_parser_exception(self):
        speg = s.SPEG()
        try:
            speg.parse_grammar('!!!')
        except Exception as ex:
            self.assertEqual(type(ex).__name__, 'GrammarParseError')

    def test_text_parser_exception(self):
        speg = s.SPEG()
        try:
            speg.parse_grammar('GRAMMAR test a -> "A";')
            speg.parse_text('B')
        except Exception as ex:
            self.assertEqual(type(ex).__name__, 'TextParseError')

    def test_grammar_before_text(self):
        speg = s.SPEG()
        try:
            speg.parse_text('B')
        except Exception as ex:
            self.assertEqual(type(ex).__name__, 'Exception')

    def test_speg_parse_grammar_parser_exception(self):
        speg = s.SPEG()
        try:
            speg.parse('!!!', 'B')
        except Exception as ex:
            self.assertEqual(type(ex).__name__, 'GrammarParseError')

    def test_speg_parse_text_parser_exception(self):
        speg = s.SPEG()
        try:
            speg.parse('GRAMMAR test a -> "A";', 'B')
        except Exception as ex:
            self.assertEqual(type(ex).__name__, 'TextParseError')
