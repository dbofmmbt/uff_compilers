from itertools import chain
from .automata import Automata
from .transition import EPSILON
from .name import Name


def parse_expression(category: str, regular_expression: str) -> Automata:
    automata = Automata()
    start = automata.add_state(category=category)

    for symbol in regular_expression:
        match symbol:
            case "(":
                pass
            case ")":
                pass
            case "|":
                pass
            case "*":
                pass
            case terminal:
                terminal_automata = Automata()
                terminal_start = terminal_automata.add_state()
                terminal_end = terminal_automata.add_state(category=category)
                terminal_automata.add_transition(
                    terminal_start.name, terminal_end.name, terminal
                )

                for final in automata.final_states():
                    automata.add_transition(final.name, terminal_start.name, EPSILON)

    return automata


def union(a: Automata, b: Automata) -> Automata:
    new_automata = Automata()

    start = new_automata.add_state()

    a_mapping = incorporate(new_automata, a)
    b_mapping = incorporate(new_automata, b)

    start.add_transition(a_mapping[a.initial_state().name], EPSILON)
    start.add_transition(b_mapping[b.initial_state().name], EPSILON)

    finals = list(new_automata.final_states())
    end = new_automata.add_state(category=next(a.final_states()).category)

    for final in finals:
        final.add_transition(end.name, EPSILON)
        final.category = None

    return new_automata


Mapping = dict[Name, Name]


def incorporate(new_automata: Automata, other: Automata) -> Mapping:
    mapping = {}

    for state in other.states.values():
        mapping[state.name] = new_automata.add_state(state.category).name

    for state in other.states.values():
        for transition in state.transitions:
            new_automata.add_transition(
                mapping[state.name], mapping[transition.destination], transition.trigger
            )

    return mapping


def concatenation(a: Automata, b: Automata) -> Automata:
    raise NotImplementedError()


def star(a: Automata) -> Automata:
    raise NotImplementedError()
