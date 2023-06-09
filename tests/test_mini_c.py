from lek.conversions import spec_to_scanner
from tests.util import check


mini_c_spec = r"""
COMPARE ==+<+>+<=+>=+!=
IF if
ELSE else

LEFT_CURLY_BRACKET {
RIGHT_CURLY_BRACKET }
LEFT_PAREN \(
RIGHT_PAREN \)
COMMA ,
SEMICOLON ;
ASSIGN =

FOR for
WHILE while

PLUS \+
MINUS -
MULT \*
DIV /

TYPE (int)+(float)
NUMBER (1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)* "not (next_symbol and next_symbol in ascii_letters)"
FLOAT (0+1+2+3+4+5+6+7+8+9)*.(0+1+2+3+4+5+6+7+8+9)* "not (next_symbol and next_symbol in ascii_letters)"
ID (\a+\A+_)(\a+\A+_+0+1+2+3+4+5+6+7+8+9)*
"""

mini_c = spec_to_scanner.convert(mini_c_spec)


def test_hello_world():
    check(
        mini_c,
        """
        int main() {
            printf(123);
        }
        """,
        """
        TYPE int
        ID main
        LEFT_PAREN (
        RIGHT_PAREN )
        LEFT_CURLY_BRACKET {
        ID printf
        LEFT_PAREN (
        NUMBER 123
        RIGHT_PAREN )
        SEMICOLON ;
        RIGHT_CURLY_BRACKET }
        """,
    )


def test_cosine_example_from_mini_c_README():
    check(
        mini_c,
        """
int main () {
  float cos, x, n, term, eps, alt;

  x = 3.14159;
  eps = 0.1;
  n = 1;
  cos = 1;
  term = 1;
  alt = -1;
  
  while (term>eps)
  {
    term = term * x * x / n / (n+1);
    cos = cos + alt * term;
    alt = -alt;
    n = n + 2;
  }
}
    """,
        """
    TYPE int
    ID main
    LEFT_PAREN (
    RIGHT_PAREN )
    LEFT_CURLY_BRACKET {
    TYPE float
    ID cos
    COMMA ,
    ID x
    COMMA ,
    ID n
    COMMA ,
    ID term
    COMMA ,
    ID eps
    COMMA ,
    ID alt
    SEMICOLON ;
    ID x
    ASSIGN =
    FLOAT 3.14159
    SEMICOLON ;
    ID eps
    ASSIGN =
    FLOAT 0.1
    SEMICOLON ;
    ID n
    ASSIGN =
    NUMBER 1
    SEMICOLON ;
    ID cos
    ASSIGN =
    NUMBER 1
    SEMICOLON ;
    ID term
    ASSIGN =
    NUMBER 1
    SEMICOLON ;
    ID alt
    ASSIGN =
    MINUS -
    NUMBER 1
    SEMICOLON ;
    WHILE while
    LEFT_PAREN (
    ID term
    COMPARE >
    ID eps
    RIGHT_PAREN )
    LEFT_CURLY_BRACKET {
    ID term
    ASSIGN =
    ID term
    MULT *
    ID x
    MULT *
    ID x
    DIV /
    ID n
    DIV /
    LEFT_PAREN (
    ID n
    PLUS +
    NUMBER 1
    RIGHT_PAREN )
    SEMICOLON ;
    ID cos
    ASSIGN =
    ID cos
    PLUS +
    ID alt
    MULT *
    ID term
    SEMICOLON ;
    ID alt
    ASSIGN =
    MINUS -
    ID alt
    SEMICOLON ;
    ID n
    ASSIGN =
    ID n
    PLUS +
    NUMBER 2
    SEMICOLON ;
    RIGHT_CURLY_BRACKET }
    RIGHT_CURLY_BRACKET }
    """,
    )
