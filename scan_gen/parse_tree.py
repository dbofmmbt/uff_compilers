from dataclasses import dataclass
from typing import Self


@dataclass
class Tree:
    Child = Self | None

    left: Child = None
    center: Child = None
    right: Child = None
    value: str | None = None
