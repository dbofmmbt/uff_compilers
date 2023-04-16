from typing import Iterator, Tuple
from .name import Name, name

from .state import State
from .token import Token
import itertools


class Automata:
    states: dict[Name, State]
    current = name(0)
    numbering_sequence: itertools.count
    word = ""
    symbols_in_process = ""

    def __init__(self):
        self.states = {}
        self.numbering_sequence = itertools.count()

    def current_state(self) -> State:
        return self.states[self.current]

    def add_state(self, state: State) -> Name:
        next_id = name(next(self.numbering_sequence))
        self.states[next_id] = state
        return next_id

    def add_transition(self, source: Name, destination: Name, trigger: str):
        self.states[source].add_transition(destination, trigger)

    def next_token(self, iterator: Iterator[str]) -> Tuple[Token, Iterator[str]] | None:
        try:
            try:
                symbol = next(iterator)
            except StopIteration:
                return

            try:
                transition = next(
                    filter(
                        lambda t: t.trigger == symbol, self.current_state().transitions
                    )
                )
                # TODO compute commit_symbols
                self.current = transition.destination
            except StopIteration:
                sink = self.current_state().sink

                if sink is not None:
                    return (
                        Token(sink, self.word),
                        itertools.chain(self.symbols_in_process, iterator),
                    )
        finally:
            self.word = ""
            self.symbols_in_process = ""
            self.current = name(0)
