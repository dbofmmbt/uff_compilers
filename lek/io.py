from lek.conversions import spec_to_scanner
from .scanner import Scanner
from .dot.automata import print_automata
import pickle


def save(scanner: Scanner, path: str):
    with open(path, "wb") as f:
        pickle.dump(scanner, f)


def load(path: str) -> Scanner:
    with open(path, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    scanner = spec_to_scanner.convert(
        """
        ANY_CATEGORY (a+b)*
        """
    )
    path = "scanner.pickle"
    save(scanner, path)
    print_automata(scanner.dfa)
    input()
    print_automata(load(path).dfa)
