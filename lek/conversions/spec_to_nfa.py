from ..spec import Spec, Entry
from ..automata_operations import union
from ..regular_expression.processor.automata import AutomataProcessor
from ..automata import Automata


def convert(spec: Spec):
    def make_automata(entry: Entry) -> Automata:
        processor = AutomataProcessor(entry.category)
        automata, _ = processor.process(entry.expression)
        return automata

    automata = make_automata(spec[0])

    for entry in spec.entries[1:]:
        current = make_automata(entry)
        automata = union(automata, current, replace_finals=False)

    return automata
