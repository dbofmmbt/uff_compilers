from lek.conversions import nfa_to_dfa, spec_to_nfa
from lek.scanner import Scanner
from tests.util import check


tokens_spec = r"""
LEFT_PAREN \( IDK
RIGHT_PAREN \) IDK
SUM \+ IDK
MULTIPLY \* IDK
NUMBER (1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)* IDK
VARIABLE \a(\a+\A)* IDK
"""

tokens_automata = spec_to_nfa.convert(tokens_spec.splitlines())
tokens_automata = nfa_to_dfa.Converter(tokens_automata).convert()
simple_tokens = Scanner(tokens_automata)


def test_parens():
    check(
        simple_tokens,
        "()",
        """
        LEFT_PAREN (
        RIGHT_PAREN )
        """,
    )


def test_number():
    check(simple_tokens, "123", "NUMBER 123")


def test_sum():
    check(simple_tokens, "+", "SUM +")


def test_multiply():
    check(simple_tokens, "*", "MULTIPLY *")


def test_variable():
    check(simple_tokens, "foo", "VARIABLE foo")


def test_math():
    check(
        simple_tokens,
        "1 + 1",
        """
        NUMBER 1
        SUM +
        NUMBER 1
        """,
    )


def test_complex_math():
    check(
        simple_tokens,
        "2 * (4+5)",
        """
        NUMBER 2
        MULTIPLY *
        LEFT_PAREN (
        NUMBER 4
        SUM +
        NUMBER 5
        RIGHT_PAREN )
        """,
    )
