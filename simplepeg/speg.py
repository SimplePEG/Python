from . import speg_visitor as sv
from . import speg_parser as sp
from . import rd_parser as rd
from . import exceptions as ex

class SPEG(object):
    def __init__(self):
        self.parser = sp.SimplePegParser()
        self.visitor = sv.SimplePegActionsVisitor(SimplePegActions())
        self.speg_parser = None

    def parse_grammar(self, grammar):
        self.speg_parser = None
        speg_ast = self.parser.parse(grammar)
        if speg_ast:
            self.speg_parser = self.visitor.visit(speg_ast)
        else:
            raise ex.GrammarParseError('Failed to parse grammar: \n\n' + self.parser.get_last_error())

    def parse_text(self, text):
        if self.speg_parser:
            rules = self.speg_parser.children
            first_rule = rules[0]
            first_rule_parser = first_rule.parser
            state = rd.State(text=text, rules=rules)
            ast = first_rule_parser(state)
            if ast:
                return ast
            else:
                raise ex.TextParseError('Failed to parse text: \n\n' + rd.get_last_error(state))
        else:
            raise Exception('You need grammar to parse text. Call parseGrammar first')

    def parse(self, grammar, text):
        speg_ast = self.parser.parse(grammar)
        if speg_ast:
            visitor = sv.SimplePegActionsVisitor(SimplePegActions())
            generated_parser = visitor.visit(speg_ast)
            rules = generated_parser.children
            first_rule = rules[0]
            first_rule_parser = first_rule.parser
            state = rd.State(text=text, rules=rules)
            ast = first_rule_parser(state)
            if ast:
                return ast
            else:
                raise ex.TextParseError('Failed to parse text: \n\n' + rd.get_last_error(state))
        else:
            raise ex.GrammarParseError('Failed to parse grammar: \n\n' + self.parser.get_last_error())


class SimplePegActions(object):
    def noop(self, node):
        return node

    def peg(self, node):
        return node.children[3]

    def parsing_body(self, node):
        node.children = [child.children[0] for child in node.children]
        return node

    def parsing_rule(self, node):
        rule = node.children[4]
        return rd.Node(
            name=node.children[0].match,
            parser=rule
        )

    def parsing_expression(self, node):
        return node.children[0]

    def parsing_sequence(self, node):
        head = [node.children[0].children[0]]
        tail = [child.children[1].children[0] for child in node.children[1].children]
        return rd.sequence(head + tail)

    def parsing_ordered_choice(self, node):
        head = [node.children[0]]
        tail = [child.children[3] for child in node.children[1].children]
        return rd.ordered_choice(head + tail)

    def parsing_sub_expression(self, node):
        return node.children[0]

    def parsing_group(self, node):
        return node.children[2]

    def parsing_atomic_expression(self, node):
        return node.children[0]

    def parsing_not_predicate(self, node):
        return rd.not_predicate(node.children[1].children[0])

    def parsing_and_predicate(self, node):
        return rd.and_predicate(node.children[1].children[0])

    def parsing_zero_or_more(self, node):
        return rd.zero_or_more(node.children[0].children[0])

    def parsing_one_or_more(self, node):
        return rd.one_or_more(node.children[0].children[0])

    def parsing_optional(self, node):
        return rd.optional(node.children[0].children[0])

    def parsing_string(self, node):
        return rd.string(node.children[1].match)

    def parsing_regex_char(self, node):
        return rd.regex_char(node.children[0].match)

    def parsing_rule_call(self, node):
        return rd.call_rule_by_name(node.match)

    def parsing_end_of_file(self, node):
        return rd.end_of_file()
