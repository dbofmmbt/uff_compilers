from dataclasses import dataclass


@dataclass
class Token:
    category: str
    value: str
    line: int
