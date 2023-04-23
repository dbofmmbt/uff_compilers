from .transition import Transition
from .name import Name


class State:
    name: Name
    transitions: list[Transition]
    category: str | None

    def __init__(self, name: Name, category: str | None = None):
        self.name = name
        self.transitions = []
        self.category = category

    def add_transition(self, destination: Name, trigger: str):
        self.transitions.append(Transition(destination, trigger))

    @property
    def is_final(self):
        return self.category is not None
