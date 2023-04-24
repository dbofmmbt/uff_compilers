from typing import Tuple

from .automata import print_automata
from .parse_tree import print_tree
from .. import machines
from ..machines import two_dots_dash
from ..parse_tree import parse_tree
from ..automata_operations import concat, star, union
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
    first = Automata()

    state0 = first.add_state()
    state1 = first.add_state(category="DOT")

    first.add_transition(state0.name, state1.name, ".")
    second = two_dots_dash()

    return first, second


def print_union():
    print_automata(union(*_two_simple_automatas()))


def print_concat():
    print_automata(concat(*_two_simple_automatas()))


def print_together():
    print_automata(*_two_simple_automatas())


def print_star():
    print_automata(*map(star, _two_simple_automatas()))


def print_parse_tree():
    result = parse_tree("(a+b)*abb")
    assert result is not None
    tree, remainder = result
    assert len(remainder) == 0
    print_tree(tree)


def print_all():
    actions = ["together", "union", "concat", "star"]

    for action in actions:
        globals()[f"print_{action}"]()
        input()
