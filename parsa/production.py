from dataclasses import dataclass


@dataclass
class Production:
    left: str
    right: list[str]

    first: set[str]
    follow: set[str]
