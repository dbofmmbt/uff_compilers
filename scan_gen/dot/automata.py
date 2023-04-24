import graphviz
from ..automata import Automata
from ..state import State


def print_automata(*automatas: Automata):
    base_graph = graphviz.Digraph()

    for idx, automata in enumerate(automatas):
        base_graph.subgraph(
            generate_graph(automata, graph_name=f"cluster_{idx}", peripheries="0")
        )

    base_graph.render(view=True, cleanup=True)


class StateInfo:
    name: str
    label: str
    peripheries: str

    def __init__(self, base_name: str, state: State):
        self.label = set_to_str(state.name)
        self.name = f"{base_name}_{self.label}"
        self.peripheries = "2" if state.is_final else "1"


def generate_graph(automata: Automata, graph_name="Automata", **attrs):
    dot = graphviz.Digraph(graph_name, graph_attr=attrs)

    set_starting_point(automata, graph_name, dot)

    for state in automata.states.values():
        state_info = StateInfo(graph_name, state)
        dot.node(**vars(state_info))

        for transition in state.transitions:
            destination = automata.states[transition.destination]
            destination_info = StateInfo(graph_name, destination)

            dot.node(**vars(destination_info))

            dot.edge(
                state_info.name,
                destination_info.name,
                transition.trigger,
            )

    return dot


def set_starting_point(automata, graph_name, dot):
    start_name = f"{graph_name}_start"
    dot.node(name=start_name, label="", shape="none", width="0", height="0")
    initial_state_info = StateInfo(graph_name, automata.initial_state())
    dot.edge(start_name, initial_state_info.name)


def set_to_str(a):
    return str(set(a))
