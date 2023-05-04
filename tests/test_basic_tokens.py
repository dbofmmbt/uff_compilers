import pytest
from lek.conversions import spec_to_scanner
from tests.util import check


tokens_spec = r"""
IF if
LEFT_PAREN \(
RIGHT_PAREN \)
SUM \+
MULTIPLY \*
NUMBER (1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)* "not (next_symbol and next_symbol in ascii_letters)"
VARIABLE \a(\a+\A)*
"""

simple_tokens = spec_to_scanner.convert(tokens_spec)


def test_parens():
    check(
        simple_tokens,
        "()",
        """
        LEFT_PAREN (
        RIGHT_PAREN )
        """,
    )


def test_if_is_recognized_as_IF():
    check(
        simple_tokens,
        "if",
        """
        IF if
        """,
    )


def test_words_with_if_preffix():
    check(
        simple_tokens,
        "ifabc",
        """
        VARIABLE ifabc
        """,
    )


def test_number():
    check(simple_tokens, "123", "NUMBER 123")


def test_number_with_letter_in_the_end_is_rejected():
    with pytest.raises(Exception) as err_info:
        check(simple_tokens, "1a", "FAILS fails")

    assert "rejected by spec" in err_info.value.args[0]


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
