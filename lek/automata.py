from typing import Iterator, Tuple
from .name import Name, name

from .state import State
from .token import Token
import itertools


class Automata:
    states: dict[Name, State]
    current = name(0)
    numbering_sequence: itertools.count

    def __init__(self):
        self.states = {}
        self.numbering_sequence = itertools.count()

    def initial_state(self) -> State:
        return self.states[name(0)]

    def current_state(self) -> State:
        return self.states[self.current]

    def category(self) -> str | None:
        return next(self.final_states()).category

    def add_state(self, category: str | None = None) -> State:
        next_id = name(next(self.numbering_sequence))
        state = State(name=next_id, category=category)
        self.states[next_id] = state
        return state

    def final_states(self) -> Iterator[State]:
        return filter(lambda s: s.is_final, self.states.values())

    def add_transition(self, source: Name, destination: Name, trigger: str):
        self.states[source].add_transition(destination, trigger)

    def next_token(self, iterator: Iterator[str]) -> Tuple[Token, Iterator[str]] | None:
        self.current = name(0)
        word = ""
        symbol = ""

        while True:
            try:
                symbol = next(iterator, "")
                transition = next(
                    t for t in self.current_state().transitions if t.trigger == symbol
                )
                self.current = transition.destination
                word += symbol
            except StopIteration:
                category = self.current_state().category

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
