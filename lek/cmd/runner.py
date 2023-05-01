import argparse
import lek.io
from ..scanner import Scanner

parser = argparse.ArgumentParser("lek runner")
parser.add_argument("automata_path")
parser.add_argument("program_path")

args = parser.parse_args()

automata = lek.io.load(args.automata_path)
scanner = Scanner(automata)


with open(args.program_path, "r") as program:
    tokens = scanner.scan(program.read())
    print(tokens)
