from .state import State
from .automata import Automata
from .state import CATEGORY_PLACEHOLDER
from .transition import EPSILON
from .name import Name


def union(a: Automata, b: Automata) -> Automata:
    new_automata = Automata()

    start = new_automata.add_state()

    a_mapping = incorporate(new_automata, a)
    b_mapping = incorporate(new_automata, b)

    start.add_transition(a_mapping[a.initial_state().name], EPSILON)
    start.add_transition(b_mapping[b.initial_state().name], EPSILON)

    finals = list(new_automata.final_states())
    end = new_automata.add_state(category=a.category())

    for final in finals:
        _make_final_go_to_other(final, end.name)

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


def _make_final_go_to_other(final: State, target: Name):
    final.add_transition(target, EPSILON)
    final.category = None


def concat(a: Automata, b: Automata) -> Automata:
    automata = Automata()

    incorporate(automata, a)

    finals = list(automata.final_states())

    b_mapping = incorporate(automata, b)

    for final in finals:
        _make_final_go_to_other(final, b_mapping[b.initial_state().name])

    return automata


def closure(a: Automata) -> Automata:
    automata = Automata()
    start = automata.add_state()
    mapping = incorporate(automata, a)

    previous_initial = automata.states[mapping[a.initial_state().name]]
    start.add_transition(previous_initial.name, EPSILON)

    finals = list(automata.final_states())
    end = automata.add_state(a.category())
    for final in finals:
        _make_final_go_to_other(final, previous_initial.name)
        _make_final_go_to_other(final, end.name)

    start.add_transition(end.name, EPSILON)

    return automata


def unit(char: str) -> Automata:
    automata = Automata()

    state0 = automata.add_state()
    state1 = automata.add_state(category=CATEGORY_PLACEHOLDER)

    automata.add_transition(state0.name, state1.name, char)

    return automata
