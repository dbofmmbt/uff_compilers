from dataclasses import dataclass
from .automata import Name

EPSILON = "ε"


@dataclass
class Transition:
    destination: Name
    trigger: str
    commit_symbols: int = 0
