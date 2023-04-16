from string import ascii_lowercase, ascii_uppercase, digits
from prolog.state import DONE, State


def dot():
    return exactly(".")


def comma():
    return exactly(",")


def left_paren():
    return exactly("(")


def right_paren():
    return exactly(")")


def exactly(char: str):
    start = State()
    end = State.final()

    start.add_transition(end, char)

    return start


def two_dots_dash():
    start = State()
    two_dots = State()
    end = State.final()

    start.add_transition(two_dots, ":")
    two_dots.add_transition(end, "-")

    return start


def query():
    start = State()
    question_mark = State()
    end = State.final()

    start.add_transition(question_mark, "?")
    question_mark.add_transition(end, "-")

    return start


def atom():
    start = State()
    loop = State()

    for char in ascii_lowercase:
        start.add_transition(loop, char)

    loop_over_identifier_ascii(loop)

    return start


def variable():
    start = State()
    loop = State()

    for char in ascii_uppercase:
        start.add_transition(loop, char)

    loop_over_identifier_ascii(loop)
    loop.fallback = DONE

    return start


def loop_over_identifier_ascii(loop):
    for char in ascii_lowercase:
        loop.add_transition(loop, char)

    for char in ascii_uppercase:
        loop.add_transition(loop, char)

    for char in digits:
        loop.add_transition(loop, char)

    loop.fallback = DONE


def numeral():
    start = State()
    loop = State()

    # Skipping '0'
    for char in digits[1:]:
        start.add_transition(loop, char)

    for char in digits:
        loop.add_transition(loop, char)

    loop.fallback = DONE

    return start
