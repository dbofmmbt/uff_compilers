from ..automata_operations import union
from ..regular_expression.processor.automata import AutomataProcessor
from ..automata import Automata


def convert(lines: list[str]):
    stripped = map(lambda l: l.strip(), lines)
    lines = list(filter(lambda l: l != "", stripped))

    def make_automata(line: str) -> Automata:
        category, expression, _ = line.split()

        processor = AutomataProcessor(category)
        automata, _ = processor.process(expression)
        return automata

    automata = make_automata(lines[0])

    for line in lines[1:]:
        current = make_automata(line)
        automata = union(automata, current, replace_finals=False)

    automata.category_priority = list(l.split()[0] for l in lines)

    return automata
