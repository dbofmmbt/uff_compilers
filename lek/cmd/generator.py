import argparse

from lek.conversions import nfa_to_dfa, spec_to_nfa

import lek.io


parser = argparse.ArgumentParser("lek generator")
parser.add_argument("input_path")
parser.add_argument("automata_path")

args = parser.parse_args()


with open(args.input_path, "r") as f:
    lines = f.readlines()

automata = spec_to_nfa.convert(lines)
automata = nfa_to_dfa.Converter(automata).convert()

lek.io.save(automata, args.automata_path)
