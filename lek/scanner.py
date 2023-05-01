import itertools
from typing import Iterator, Tuple

from .token import Token
from .automata import Automata


class Scanner:
    def __init__(self, dfa: Automata) -> None:
        self.dfa = dfa

    def scan(self, input: str) -> list[Token]:
        tokens = []

        iter = input.__iter__()

        while token := self.next_token(iter):
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
