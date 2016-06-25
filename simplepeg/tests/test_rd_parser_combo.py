from unittest import TestCase

from .. import rd_parser as rd
from .. import speg_visitor as sv


class TestRDParserCombinations(TestCase):
    def test_simple_math_grammar(self):
        def space():
            return rd.regex_char('[\\s]')

        def multiplicative():
            return rd.string('*')

        def additive():
            return rd.string('+')

        def factor():
            return rd.ordered_choice([
                rd.sequence([
                    rd.string('('),
                    rd.rec(exp),
                    rd.string(')')
                ]),
                rd.regex_char('[0-9]')
            ])

        def term():
            return rd.sequence([
                factor(),
                rd.zero_or_more(rd.sequence([
                    space(),
                    multiplicative(),
                    space(),
                    factor()
                ]))
            ])

        def exp():
            return rd.sequence([
                term(),
                rd.zero_or_more(rd.sequence([
                    space(),
                    additive(),
                    space(),
                    term()
                ]))
            ])

        def math():
            return rd.sequence([
                exp(),
                rd.end_of_file()
            ])
        parser = math()
        ast = parser(rd.State(
            text='1 + 2'
        ))
        self.assertEqual(ast.match, '1 + 2')
        visitor = sv.PegJsVisitor()
        pegjs_ast = visitor.visit(ast)
        self.assertEqual(pegjs_ast, [[[['1'], []], [[' ', '+', ' ', [['2'], []]]]], None])
