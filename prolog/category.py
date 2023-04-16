from dataclasses import dataclass
from prolog.state import State


@dataclass
class Category:
    label: str
    machine: State
