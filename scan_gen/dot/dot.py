from typing import Tuple
from scan_gen.conversions import nfa_to_dfa

from scan_gen.regular_expression.processor import ParseTreeProcessor
from ..regular_expression.processor.automata import AutomataProcessor

from .automata import print_automata
from .parse_tree import print_tree
from .. import machines
from ..machines import two_dots_dash
from ..automata_operations import concat, closure, union, unit
from ..automata import Automata


def example_automatas():
    return [
        ("DOT", machines.dot()),
        ("COMMA", machines.comma()),
        ("TWO_DOTS_SLASH", machines.two_dots_dash()),
        ("QUERY", machines.query()),
        ("LEFT_PAREN", machines.left_paren()),
        ("RIGHT_PAREN", machines.right_paren()),
        ("ATOM", machines.atom()),
        ("VARIABLE", machines.variable()),
        ("NUMERAL", machines.numeral()),
    ]


def _two_simple_automatas() -> Tuple[Automata, Automata]:
    first = unit(".")
    second = two_dots_dash()

    return first, second


def print_union():
    print_automata(union(*_two_simple_automatas()))


def print_concat():
    print_automata(concat(*_two_simple_automatas()))


def print_together():
    print_automata(*_two_simple_automatas())


def print_star():
    print_automata(*map(closure, _two_simple_automatas()))


expression = "(a+bc)*abb"


def print_nfa():
    processor = AutomataProcessor("CATEGORIA BOLADA")
    automata, _ = processor.process(expression)
    print_automata(automata)


def print_dfa():
    processor = AutomataProcessor("CATEGORIA BOLADA")
    automata, _ = processor.process(expression)

    print_automata(nfa_to_dfa.Converter(automata).convert())


def print_parse_tree():
    processor = ParseTreeProcessor()
    result = processor.process(expression)
    assert result is not None
    tree, remainder = result
    assert len(remainder) == 0
    print_tree(tree)


def print_all():
    actions = ["together", "union", "concat", "star"]

    for action in actions:
        globals()[f"print_{action}"]()
        input()
