import argparse

from lek.conversions import spec_to_scanner
import lek.io


parser = argparse.ArgumentParser("lek generator")
parser.add_argument("input_path")
parser.add_argument("scanner_path")

args = parser.parse_args()


with open(args.input_path, "r") as f:
    input = f.read()

scanner = spec_to_scanner.convert(input)

lek.io.save(scanner, args.scanner_path)
