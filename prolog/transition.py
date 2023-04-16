from dataclasses import dataclass
from prolog.state import State


@dataclass
class Transition:
    destination: State
    trigger: str
