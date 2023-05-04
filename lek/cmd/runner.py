import argparse
import lek.io

parser = argparse.ArgumentParser("lek runner")
parser.add_argument("scanner_path")
parser.add_argument("program_path")

args = parser.parse_args()

scanner = lek.io.load(args.scanner_path)


with open(args.program_path, "r") as program:
    tokens = scanner.scan(program.read())
    print(tokens)
