from dataclasses import dataclass


@dataclass
class Entry:
    category: str
    expression: str
    acceptance_code: str | None = None


class Spec:
    entries: list[Entry]

    def __init__(self, lines: list[str]):
        stripped = map(lambda l: l.strip(), lines)
        lines = list(filter(lambda l: l != "", stripped))

        entries = []

        for line in lines:
            category, expression, *rest = line.split()

            rejection_code = " ".join(rest).strip('"')
            entries.append(Entry(category, expression, rejection_code or None))

        self.entries = entries

    def priority(self) -> list[str]:
        return list(e.category for e in self.entries)

    def acceptance_code(self, category: str) -> str:
        return next(
            e.acceptance_code or "True" for e in self.entries if e.category == category
        )

    def __getitem__(self, item):
        return self.entries[item]
