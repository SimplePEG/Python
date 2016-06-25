"""Recursive decent parser"""
# pylint: disable=too-few-public-methods

import json
import re


class State(object):
    """Current parser state"""
    text = ""
    position = 0
    rules = []
    last_expectations = []

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_json(self):
        """returns json string"""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)


class Node(object):
    """Node of AST"""
    match = ""
    children = None
    action = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_json(self):
        """returns json string"""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)


class Expectation(object):
    """Expectation object"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_json(self):
        """returns json string"""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)


def get_last_error(state):
    if len(state.last_expectations) < 1:
        return False
    lines = state.text.split('\n')
    last_exp_position = max([exp.position for exp in state.last_expectations])
    last_position = 0
    line_of_error = ''
    error_line_number = None
    position_of_error = 0
    i = 0
    while i < len(lines):
        line_lenght = len(lines[i]) + 1
        if last_position <= last_exp_position < last_position + line_lenght:
            line_of_error = lines[i]
            position_of_error = last_exp_position - last_position
            error_line_number = i + 1
            break
        last_position += line_lenght
        i += 1
    str_error_ln = str(error_line_number)
    error_ln_length = len(str_error_ln)
    unexpected_char = 'EOF'
    if last_exp_position < len(state.text):
        unexpected_char = state.text[last_exp_position]
    unexpected = 'Unexpected "' + unexpected_char + '"'
    expected_rules = [exp.rule for exp in state.last_expectations]
    expected = ' expected (' + ' or '.join(expected_rules) + ')'
    pointer = ('-'*(position_of_error + 2 + error_ln_length)) + '^'
    extra = line_of_error + '\n' + pointer
    return unexpected + expected + '\n' + str_error_ln + ': ' + extra


def string(rule):
    def _(state):
        state.last_expectations = []
        if state.text[state.position:state.position+len(rule)] == rule:
            start_position = state.position
            state.position += len(rule)
            return Node(
                type='string',
                match=rule,
                start_position=start_position,
                end_position=state.position
            )
        else:
            state.last_expectations = [Expectation(
                type='string',
                rule=rule,
                position=state.position
            )]
            return False
    return _


def regex_char(rule):
    def _(state):
        state.last_expectations = []
        match = re.match(rule, state.text[state.position:])
        if match and match.start() == 0:
            start_position = state.position
            state.position += match.end()
            return Node(
                type='regex_char',
                match=match.group(0),
                start_position=start_position,
                end_position=state.position
            )
        else:
            state.last_expectations = [Expectation(
                type='regex_char',
                rule=rule,
                position=state.position
            )]
            return False
    return _


def sequence(parsers):
    def _(state):
        asts = []
        start_position = state.position
        i = 0
        while i < len(parsers):
            ast = parsers[i](state)
            if ast:
                asts.append(ast)
            else:
                return False
            i += 1
        match = ''.join([(ast.match if ast.match is not None else '') for ast in asts])
        return Node(
            type='sequence',
            match=match,
            children=asts,
            start_position=start_position,
            end_position=state.position
        )
    return _


def ordered_choice(parsers):
    def _(state):
        expectations = []
        initial_text = state.text
        initial_position = state.position
        i = 0
        while i < len(parsers):
            ast = parsers[i](state)
            if ast:
                return Node(
                    type='ordered_choice',
                    match=ast.match,
                    children=[ast],
                    start_position=initial_position,
                    end_position=state.position,
                )
            else:
                state.text = initial_text
                state.position = initial_position
                expectations = expectations + state.last_expectations
            i += 1
        state.last_expectations = expectations
        return False
    return _


def zero_or_more(parser):
    def _(state):
        asts = []
        start_position = state.position
        ast = True
        while ast:
            state_position = state.position
            ast = parser(state)
            if ast:
                asts.append(ast)
            else:
                state.position = state_position
        state.last_expectations = []
        match = ''.join([(ast.match if ast.match is not None else '') for ast in asts])
        return Node(
            type='zero_or_more',
            match=match,
            children=asts,
            start_position=start_position,
            end_position=state.position
        )
    return _


def one_or_more(parser):
    def _(state):
        asts = []
        start_position = state.position
        ast = True
        while ast:
            state_position = state.position
            ast = parser(state)
            if ast:
                asts.append(ast)
            else:
                state.position = state_position
        if len(asts) > 0:
            state.last_expectations = []
            match = ''.join([(ast.match if ast.match is not None else '') for ast in asts])
            return Node(
                type='one_or_more',
                match=match,
                children=asts,
                start_position=start_position,
                end_position=state.position
            )
        else:
            return False
    return _


def optional(parser):
    def _(state):
        start_position = state.position
        match = None
        children = None
        ast = parser(state)
        if ast:
            match = ast.match
            children = [ast]
        return Node(
            type='optional',
            match=match,
            children=children,
            start_position=start_position,
            end_position=state.position
        )
    return _


def and_predicate(parser):
    def _(state):
        current_text = state.text
        current_position = state.position
        ast = parser(state)
        if ast:
            state.text = current_text
            state.position = current_position
            return Node(
                type='and_predicate',
                match=None,
                children=[ast],
                start_position=state.position,
                end_position=state.position
            )
        else:
            return False
    return _


def not_predicate(parser):
    def _(state):
        current_text = state.text
        current_position = state.position
        ast = parser(state)
        if ast:
            state.text = current_text
            state.position = current_position
            state.last_expectations = [Expectation(
                type='not_predicate',
                children=[ast],
                position=state.position
            )]
            return False
        else:
            state.last_expectations = []
            return Node(
                type='not_predicate',
                match=None,
                children=[],
                start_position=state.position,
                end_position=state.position
            )
    return _


def end_of_file():
    def _(state):
        if len(state.text) == state.position:
            return Node(
                type='end_of_file',
                match=None,
                children=[],
                start_position=state.position,
                end_position=state.position
            )
        else:
            state.last_expectations = [Expectation(
                type='end_of_file',
                rule='EOF',
                position=state.position
            )]
            return False
    return _


def rec(func):
    """Allows you to do recursive currying"""
    def _(*args, **kwargs):
        return func()(*args, **kwargs)
    return _


def action(name, func):
    def _(*args, **kwargs):
        ast = func(*args, **kwargs)
        if ast:
            ast.action = name
        return ast
    return _


def call_rule_by_name(name):
    def _(state):
        rule = next((x for x in state.rules if x.name == name), None)
        ast = rule.parser(state)
        return ast
    return _
