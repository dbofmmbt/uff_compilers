from lek.conversions import nfa_to_dfa, spec_to_nfa
from lek.scanner import Scanner
from tests.util import check


prolog_spec = r"""
LEFT_PAREN \( IDK
RIGHT_PAREN \) IDK
QUERY ?- IDK
VARIABLE (A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z)((A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z+a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z)*) IDK
ATOM (a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z)((A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z+a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z)*) IDK
NUMBER (1+2+3+4+5+6+7+8+9)((0+1+2+3+4+5+6+7+8+9)*) IDK
"""

prolog_automata = spec_to_nfa.convert(prolog_spec.splitlines())
prolog_automata = nfa_to_dfa.Converter(prolog_automata).convert()
prolog = Scanner(prolog_automata)


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
