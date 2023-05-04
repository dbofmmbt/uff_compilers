from dataclasses import dataclass


@dataclass
class Entry:
    category: str
    expression: str
    rejection_code: str


class Spec:
    entries: list[Entry]

    def __init__(self, lines: list[str]):
        stripped = map(lambda l: l.strip(), lines)
        lines = list(filter(lambda l: l != "", stripped))

        self.entries = list(Entry(*line.split()) for line in lines)

    def priority(self) -> list[str]:
        return list(e.category for e in self.entries)

    def rejection_code(self, category: str) -> str:
        return next(e.rejection_code for e in self.entries if e.category == category)

    def __getitem__(self, item):
        return self.entries[item]
