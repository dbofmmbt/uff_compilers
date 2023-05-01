from lek.conversions import nfa_to_dfa, spec_to_nfa
from lek.scanner import Scanner


prolog = r"""
LEFT_PAREN \( IDK
RIGHT_PAREN \) IDK
QUERY ?- IDK
VARIABLE (A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z)((A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z+a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z)*) IDK
ATOM (a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z)((A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z+a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z)*) IDK
NUMBER (1+2+3+4+5+6+7+8+9)((0+1+2+3+4+5+6+7+8+9)*) IDK
"""

prolog_automata = spec_to_nfa.convert(prolog.splitlines())
prolog_automata = nfa_to_dfa.Converter(prolog_automata).convert()
prolog_scanner = Scanner(prolog_automata)


def check(source: str, expected: str):
    tokens = list(map(lambda t: (t.category, t.value), prolog_scanner.scan(source)))

    expected_tokens = []

    for line in filter(lambda l: l.strip() != "", expected.splitlines()):
        category, value = line.split()
        expected_tokens.append((category, value))

    assert tokens == expected_tokens


def test_parens():
    check(
        "()",
        """
        LEFT_PAREN (
        RIGHT_PAREN )
        """,
    )


def test_atom():
    check("abcd", "ATOM abcd")


def test_atom_and_variable():
    check(
        "abc Abc",
        """
        ATOM abc
        VARIABLE Abc
        """,
    )


def test_number():
    check("123", "NUMBER 123")


def test_number_with_others():
    check(
        "Variable 128 atom",
        """
        VARIABLE Variable
        NUMBER 128
        ATOM atom
        """,
    )
