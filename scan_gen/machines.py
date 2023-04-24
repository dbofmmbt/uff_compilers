import itertools
from string import ascii_lowercase, ascii_uppercase, digits

from .state import State
from .automata import Automata


def dot():
    return exactly(".")


def comma():
    return exactly(",")


def left_paren():
    return exactly("(")


def right_paren():
    return exactly(")")


def exactly(char: str):
    automata = Automata()

    start = automata.add_state()
    end = automata.add_state(category=char)

    automata.add_transition(start.name, end.name, char)

    return automata


def two_dots_dash():
    automata = Automata()
    start = automata.add_state()
    two_dots = automata.add_state()
    end = automata.add_state(category="TWO_DOTS_DASH")

    automata.add_transition(start.name, two_dots.name, ":")
    automata.add_transition(two_dots.name, end.name, "-")

    return automata


def query():
    automata = Automata()
    start = automata.add_state()
    question_mark = automata.add_state()
    end = automata.add_state(category="QUERY")

    automata.add_transition(start.name, question_mark.name, "?")
    automata.add_transition(question_mark.name, end.name, "-")

    return automata


def atom():
    automata = Automata()
    start = automata.add_state()
    loop = automata.add_state(category="ATOM")

    for char in ascii_lowercase:
        automata.add_transition(start.name, loop.name, char)

    loop_over_identifier_ascii(automata, loop)

    return automata


def variable():
    automata = Automata()
    start = automata.add_state()
    loop = automata.add_state(category="VARIABLE")

    for char in ascii_uppercase:
        automata.add_transition(start.name, loop.name, char)

    loop_over_identifier_ascii(automata, loop)

    return automata


def loop_over_identifier_ascii(automata: Automata, loop: State):
    name = loop.name

    def create_loop(char):
        automata.add_transition(name, name, char)

    for char in itertools.chain(ascii_lowercase, ascii_uppercase, digits):
        create_loop(char)


def numeral():
    automata = Automata()
    start = automata.add_state()
    loop = automata.add_state(category="NUMERAL")

    # Skipping '0'
    for char in digits[1:]:
        automata.add_transition(start.name, loop.name, char)

    for char in digits:
        automata.add_transition(loop.name, loop.name, char)

    return automata
