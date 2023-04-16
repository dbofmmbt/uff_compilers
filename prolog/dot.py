import graphviz
from .automata import Automata


def print_automata(automata: Automata):
    dot = graphviz.Digraph("Automata")

    for id, state in automata.states.items():
        dot.node(set_to_str(id))

        for transition in state.transitions:
            dot.edge(
                set_to_str(id), set_to_str(transition.destination), transition.trigger
            )
        sink_label = state.sink or "failure"
        dot.node(sink_label, peripheries="2")
        dot.edge(set_to_str(id), sink_label, "otherwise")

    dot.render(view=True)


def set_to_str(a):
    return str(set(a))


if __name__ == "__main__":
    from .automata import Automata
    from .state import State

    automata = Automata()

    state0 = State()
    state1 = State(sink="DOT")
    id0 = automata.add_state(state0)
    id1 = automata.add_state(state1)

    automata.add_transition(id0, id1, ".", commit_symbols=1)

    print_automata(automata)
