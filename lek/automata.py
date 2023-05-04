from typing import Iterator
from .name import Name, name

from .state import State
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
