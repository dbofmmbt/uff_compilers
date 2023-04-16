from .transition import Transition
from .automata import Name


class State:
    transitions: list[Transition]
    sink: str | None

    def __init__(
        self, sink: str | None = None, transitions: list[Transition] | None = None
    ):
        self.sink = sink
        self.transitions = transitions if transitions is not None else []

    def add_transition(self, destination: Name, trigger: str):
        self.transitions.append(Transition(destination, trigger))
