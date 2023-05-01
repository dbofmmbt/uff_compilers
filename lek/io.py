from .dot.automata import print_automata
from .regular_expression.processor.automata import AutomataProcessor
from .automata import Automata
import pickle


def save(automata: Automata, path: str):
    with open(path, "wb") as f:
        pickle.dump(automata, f)


def load(path: str) -> Automata:
    with open(path, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    processor = AutomataProcessor("any category")
    automata, _ = processor.process("(a+b)*")

    path = "automata.pickle"
    save(automata, path)
    print_automata(automata)
    input()
    print_automata(load(path))
