from . import rd_parser as rd


def peg():
    return rd.action('peg', rd.sequence([
        rd.zero_or_more(_()),
        parsing_header(),
        rd.one_or_more(_()),
        parsing_body(),
        rd.end_of_file()
    ]))


def parsing_header():
    return rd.action('noop', rd.sequence([
        rd.string('GRAMMAR'),
        rd.one_or_more(_()),
        rd.one_or_more(parsing_rule_name())
    ]))


def parsing_body():
    return rd.action('parsing_body', rd.one_or_more(rd.ordered_choice([
        parsing_rule(),
        rd.one_or_more(_())
    ])))


def parsing_rule():
    return rd.action('parsing_rule', rd.sequence([
        parsing_rule_name(),
        rd.zero_or_more(_()),
        rd.string('->'),
        rd.zero_or_more(_()),
        parsing_expression(),
        rd.zero_or_more(_()),
        rd.string(';'),
        rd.zero_or_more(_())
    ]))


def parsing_rule_name():
    return rd.action('noop', rd.sequence([
        rd.regex_char('[a-zA-Z]'),
        rd.zero_or_more(rd.regex_char('[a-zA-Z_]')),
    ]))


def parsing_expression():
    return rd.action('parsing_expression', rd.ordered_choice([
        parsing_sequence(),
        parsing_ordered_choice(),
        parsing_sub_expression()
    ]))


def parsing_sequence():
    return rd.action('parsing_sequence', rd.sequence([
        rd.ordered_choice([
            parsing_ordered_choice(),
            parsing_sub_expression()
        ]),
        rd.one_or_more(rd.sequence([
            rd.one_or_more(_()),
            rd.ordered_choice([
                parsing_ordered_choice(),
                parsing_sub_expression()
            ])
        ]))
    ]))


def parsing_ordered_choice():
    return rd.action('parsing_ordered_choice', rd.sequence([
        parsing_sub_expression(),
        rd.one_or_more(rd.sequence([
            rd.zero_or_more(_()),
            rd.string('/'),
            rd.zero_or_more(_()),
            parsing_sub_expression(),
        ]))
    ]))


def parsing_sub_expression():
    return rd.action('parsing_sub_expression', rd.ordered_choice([
        parsing_not_predicate(),
        parsing_and_predicate(),
        parsing_optional(),
        parsing_one_or_more(),
        parsing_zero_or_more(),
        parsing_group(),
        parsing_atomic_expression()
    ]))


def parsing_group():
    return rd.action('parsing_group', rd.sequence([
        rd.string('('),
        rd.zero_or_more(_()),
        rd.rec(parsing_expression),
        rd.zero_or_more(_()),
        rd.string(')')
    ]))


def parsing_atomic_expression():
    return rd.action('parsing_atomic_expression', rd.ordered_choice([
        parsing_string(),
        parsing_regex_char(),
        parsing_eof(),
        parsing_rule_call()
    ]))


def parsing_not_predicate():
    return rd.action('parsing_not_predicate', rd.sequence([
        rd.string('!'),
        rd.ordered_choice([
            parsing_group(),
            parsing_atomic_expression()
        ])
    ]))


def parsing_and_predicate():
    return rd.action('parsing_and_predicate', rd.sequence([
        rd.string('&'),
        rd.ordered_choice([
            parsing_group(),
            parsing_atomic_expression()
        ])
    ]))


def parsing_zero_or_more():
    return rd.action('parsing_zero_or_more', rd.sequence([
        rd.ordered_choice([
            parsing_group(),
            parsing_atomic_expression()
        ]),
        rd.string('*')
    ]))


def parsing_one_or_more():
    return rd.action('parsing_one_or_more', rd.sequence([
        rd.ordered_choice([
            parsing_group(),
            parsing_atomic_expression()
        ]),
        rd.string('+')
    ]))


def parsing_optional():
    return rd.action('parsing_optional', rd.sequence([
        rd.ordered_choice([
            parsing_group(),
            parsing_atomic_expression()
        ]),
        rd.string('?')
    ]))


def parsing_rule_call():
    return rd.action('parsing_rule_call', parsing_rule_name())


def parsing_string():
    return rd.action('parsing_string', rd.sequence([
        rd.string('"'),
        rd.one_or_more(rd.ordered_choice([
            rd.string('\\"'),
            rd.regex_char('[^"]'),
        ])),
        rd.string('"')
    ]))


def parsing_regex_char():
    return rd.action('parsing_regex_char', rd.ordered_choice([
        rd.sequence([
            rd.string('['),
            rd.optional(rd.string('^')),
            rd.one_or_more(rd.ordered_choice([
                rd.string('\\]'),
                rd.string('\\['),
                rd.regex_char('[^\\]]'),
            ])),
            rd.string(']')
        ]),
        rd.string('.')
    ]))


def parsing_eof():
    return rd.action('parsing_end_of_file', rd.string("EOF"))


def _():
    return rd.action('noop', rd.regex_char('[\\s]'))


class SimplePegParser(object):
    """Class that allows you to parse PEG grammaras (EBNF-ish style)"""
    parser = None
    state = None

    def __init__(self):
        self.parser = peg()

    def parse(self, text):
        self.state = rd.State(
            text=text,
            position=0
        )
        ast = self.parser(self.state)
        return ast

    def get_last_expectations(self):
        return self.state.last_expectations

    def get_last_error(self):
        return rd.get_last_error(self.state)
