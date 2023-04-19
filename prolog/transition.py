from dataclasses import dataclass
from .name import Name

EPSILON = "ε"


@dataclass
class Transition:
    destination: Name
    trigger: str
