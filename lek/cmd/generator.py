import argparse

from lek.conversions import nfa_to_dfa

from ..automata_operations import union
from ..regular_expression.processor.automata import AutomataProcessor
from ..automata import Automata
import lek.io


parser = argparse.ArgumentParser("lek generator")
parser.add_argument("input_path")
parser.add_argument("automata_path")

args = parser.parse_args()


def make_automata(line: str) -> Automata:
    category, expression, _ = line.split()

    processor = AutomataProcessor(category)
    automata, _ = processor.process(expression)
    return automata


with open(args.input_path, "r") as f:
    stripped_lines = map(lambda l: l.strip(), f.readlines())
    lines = list(l for l in stripped_lines if l != "")

automata = make_automata(lines[0])

for line in lines[1:]:
    current = make_automata(line)
    automata = union(automata, current, replace_finals=False)


automata = nfa_to_dfa.Converter(automata).convert()

lek.io.save(automata, args.automata_path)
