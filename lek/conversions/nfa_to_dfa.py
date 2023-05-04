from contextlib import suppress
from string import printable
from typing import Iterable, Tuple
from ..name import Name
from ..transition import EPSILON
from ..automata import Automata


class Converter:
    def __init__(self, nfa: Automata):
        self.nfa = nfa

    def convert(self) -> Automata:
        dfa = Automata()
        mapping: dict[frozenset[Name], Name] = dict()

        def propagate_final(state_set: frozenset[Name]):
            set_categories = set(self.nfa.states[name].category for name in state_set)

            first_in_priority = None
            # checking in asceding order
            for category in self.nfa.category_priority:
                if category in set_categories:
                    first_in_priority = category
                    break
            if first_in_priority is None:
                return

            state_in_dfa = dfa.states[mapping[state_set]]
            state_in_dfa.category = first_in_priority

        def ensure_state_is_mapped(state_set: frozenset[Name]):
            if mapping.get(state_set) is None:
                new_state = dfa.add_state()
                mapping[state_set] = new_state.name
                propagate_final(state_set)

        initial_state, states, transitions = self.subset_construction()
        ensure_state_is_mapped(initial_state)

        for source in states:
            ensure_state_is_mapped(source)

            for (transition_state, trigger), destination in transitions.items():
                if transition_state == source:
                    ensure_state_is_mapped(destination)
                    dfa.add_transition(mapping[source], mapping[destination], trigger)

        return dfa

    def state_closure(self, name: Name) -> frozenset[Name]:
        to_visit = [name]
        closure: set[Name] = {name}

        while to_visit:
            current = self.nfa.states[to_visit.pop()]
            epsilon_destinations = (
                t.destination for t in current.transitions if t.trigger == EPSILON
            )

            for destination in epsilon_destinations:
                if destination not in closure:
                    to_visit.append(destination)
                    closure.add(destination)

        return frozenset(closure)

    def set_closure(self, names: frozenset[Name]) -> frozenset[Name]:
        closures = (self.state_closure(name) for name in names)
        return frozenset().union(*closures)

    def move(self, names: frozenset[Name], symbol: str) -> frozenset[Name]:
        reachable: set[Name] = set()

        for name in names:
            state = self.nfa.states[name]

            reachable_through_symbol = (
                t.destination for t in state.transitions if t.trigger == symbol
            )

            reachable = reachable.union(reachable_through_symbol)

        return frozenset(reachable)

    def subset_construction(self):
        start_state = self.state_closure(self.nfa.initial_state().name)
        dfa_states: set[frozenset[Name]] = set([start_state])
        dfa_unmarked_states = dfa_states.copy()
        dfa_transitions: dict[Tuple[frozenset[Name], str], frozenset[Name]] = dict()

        while dfa_unmarked_states:
            current = dfa_unmarked_states.pop()

            for symbol in printable:
                destination = self.set_closure(self.move(current, symbol))

                if len(destination) == 0:
                    continue

                if destination not in dfa_states:
                    dfa_states.add(destination)
                    dfa_unmarked_states.add(destination)
                dfa_transitions[current, symbol] = destination

        return start_state, dfa_states, dfa_transitions
