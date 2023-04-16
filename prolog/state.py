from typing import Self
from prolog.transition import Transition


class State:
    transitions: set[Transition] = {}
    is_final: bool = False
    fallback: Self

    def __init__(self):
        self.fallback = VOID

    def add_transition(self, destination: Self, trigger: str):
        self.transitions.add(Transition(
            destination=destination, trigger=trigger))

    def apply_input(self, next_element: str) -> Self:
        for transition in self.transitions:
            if transition == next_element:
                return transition.destination

        return self.fallback

    @staticmethod
    def final():
        s = State()
        s.is_final = True
        return s


# Transition-less non-final state
VOID = State()
DONE = State.final()
