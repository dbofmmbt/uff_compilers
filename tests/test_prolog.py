from lek.conversions import spec_to_scanner
from tests.util import check


prolog_spec = r"""
LEFT_PAREN \(
RIGHT_PAREN \)

QUERY ?-
DOT .
COMMA ,
RULE :-

VARIABLE \A(\a+\A)*
ATOM \a(\a+\A)*
NUMBER (1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)* "not (next_symbol and next_symbol in ascii_letters)"
"""

prolog = spec_to_scanner.convert(prolog_spec)


def test_atom():
    check(prolog, "abcd", "ATOM abcd")


def test_atom_and_variable():
    check(
        prolog,
        "abc Abc",
        """
        ATOM abc
        VARIABLE Abc
        """,
    )


def test_number_with_others():
    check(
        prolog,
        "Variable 128 atom",
        """
        VARIABLE Variable
        NUMBER 128
        ATOM atom
        """,
    )


def test_fact():
    check(
        prolog,
        "food(burger).",
        """
        ATOM food
        LEFT_PAREN (
        ATOM burger
        RIGHT_PAREN )
        DOT .
        """,
    )


def test_rule():
    check(
        prolog,
        "meal(X) :- food(X).",
        """
        ATOM meal
        LEFT_PAREN (
        VARIABLE X
        RIGHT_PAREN )
        RULE :-
        ATOM food
        LEFT_PAREN (
        VARIABLE X
        RIGHT_PAREN )
        DOT .
        """,
    )


def test_query():
    check(
        prolog,
        "?- food(pizza).",
        """
        QUERY ?-
        ATOM food
        LEFT_PAREN (
        ATOM pizza
        RIGHT_PAREN )
        DOT .
        """,
    )


def test_query_with_more_than_one_clause():
    check(
        prolog,
        "?- meal(X), lunch(X).",
        """
        QUERY ?-
        ATOM meal
        LEFT_PAREN (
        VARIABLE X
        RIGHT_PAREN )
        COMMA ,
        ATOM lunch
        LEFT_PAREN (
        VARIABLE X
        RIGHT_PAREN )
        DOT .
        """,
    )


def test_professor_query():
    check(
        prolog,
        "professor(X, Y) :- teaches(X, C), studies(Y, C).",
        """
        ATOM professor
        LEFT_PAREN (
        VARIABLE X
        COMMA ,
        VARIABLE Y
        RIGHT_PAREN )
        RULE :-
        ATOM teaches
        LEFT_PAREN (
        VARIABLE X
        COMMA ,
        VARIABLE C
        RIGHT_PAREN )
        COMMA ,
        ATOM studies
        LEFT_PAREN (
        VARIABLE Y
        COMMA ,
        VARIABLE C
        RIGHT_PAREN )
        DOT .
        """,
    )


def test_students_query():
    check(
        prolog,
        "?- professor(kirke, Students).",
        """
        QUERY ?-
        ATOM professor
        LEFT_PAREN (
        ATOM kirke
        COMMA ,
        VARIABLE Students
        RIGHT_PAREN )
        DOT .
        """,
    )
