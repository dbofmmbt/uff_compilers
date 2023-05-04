from lek.conversions import nfa_to_dfa, spec_to_nfa
from ..scanner import Scanner
from ..spec import Spec


def convert(input: str):
    spec = Spec(input.splitlines())
    nfa = spec_to_nfa.convert(spec)
    dfa = nfa_to_dfa.Converter(nfa, spec).convert()
    return Scanner(dfa, spec)
