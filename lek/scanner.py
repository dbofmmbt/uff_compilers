import itertools
from string import ascii_letters, punctuation, whitespace

from typing import Iterator, Tuple

from .spec import Spec

from .token import Token
from .automata import Automata


class Scanner:
    def __init__(self, dfa: Automata, spec: Spec) -> None:
        self.dfa = dfa
        self.spec = spec

    def scan(self, input: str) -> list[Token]:
        tokens = []

        iter = input.__iter__()

        while result := self.next_token(iter):
            token, iter = result
            tokens.append(token)

        self.dfa.current = self.dfa.initial_state().name

        return tokens

    def next_token(self, iterator: Iterator[str]) -> Tuple[Token, Iterator[str]] | None:
        self.dfa.current = self.dfa.initial_state().name
        word = ""
        symbol = ""

        while True:
            try:
                symbol = next(iterator, "")
                transition = next(
                    t
                    for t in self.dfa.current_state().transitions
                    if t.trigger == symbol
                )
                self.dfa.current = transition.destination
                word += symbol
            except StopIteration:
                category = self.dfa.current_state().category

                if category is not None:
                    if not eval(
                        self.spec.acceptance_code(category),
                        {},
                        {
                            "next_symbol": symbol,
                            "ascii_letters": ascii_letters,
                            "whitespace": whitespace,
                            "punctuation": punctuation,
                        },
                    ):
                        raise Exception(f"Token rejected by spec: {word + symbol}")

                    return (
                        Token(category, word),
                        itertools.chain(symbol, iterator),
                    )
                else:
                    match symbol:
                        case "":
                            # end of input
                            return None
                        case " " | "\n":
                            # just ignore those chars for now
                            pass
                        case _:
                            raise Exception(f"Invalid token found: {word}")
