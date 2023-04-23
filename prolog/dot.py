from itertools import count
from typing import Tuple
import graphviz
from prolog import machines

from prolog.machines import two_dots_dash
from prolog.parse_tree import Tree, parse_tree
from prolog.regular_expression import concat, star, union
from prolog.state import State
from .automata import Automata


def example_automatas():
    return [
        ("DOT", machines.dot()),
        ("COMMA", machines.comma()),
        ("TWO_DOTS_SLASH", machines.two_dots_dash()),
        ("QUERY", machines.query()),
        ("LEFT_PAREN", machines.left_paren()),
        ("RIGHT_PAREN", machines.right_paren()),
        ("ATOM", machines.atom()),
        ("VARIABLE", machines.variable()),
        ("NUMERAL", machines.numeral()),
    ]


def print_automata(*automatas: Automata):
    base_graph = graphviz.Digraph()

    for idx, automata in enumerate(automatas):
        base_graph.subgraph(
            generate_graph(automata, graph_name=f"cluster_{idx}", peripheries="0")
        )

    base_graph.render(view=True, cleanup=True)


class NodeInfo:
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
        state_info = NodeInfo(graph_name, state)
        dot.node(**vars(state_info))

        for transition in state.transitions:
            destination = automata.states[transition.destination]
            destination_info = NodeInfo(graph_name, destination)

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
    initial_state_info = NodeInfo(graph_name, automata.initial_state())
    dot.edge(start_name, initial_state_info.name)


def set_to_str(a):
    return str(set(a))


def two_simple_automatas() -> Tuple[Automata, Automata]:
    first = Automata()

    state0 = first.add_state()
    state1 = first.add_state(category="DOT")

    first.add_transition(state0.name, state1.name, ".")
    second = two_dots_dash()

    return first, second


def print_union():
    print_automata(union(*two_simple_automatas()))


def print_concat():
    print_automata(concat(*two_simple_automatas()))


def print_together():
    print_automata(*two_simple_automatas())


def print_star():
    print_automata(*map(star, two_simple_automatas()))


def print_tree(tree: Tree):
    graph = graphviz.Graph()
    internal_node_count = count()
    leaf_node_count = count(start=10_000)

    def make_name(count):
        return str(next(count))

    root_name = make_name(internal_node_count)
    nodes: list[Tuple[str, Tree.Child]] = [(root_name, tree)]
    graph.node(root_name, label=f"r{root_name}")

    while nodes:
        current_name, current = nodes.pop(0)

        if isinstance(current, str):
            graph.node(name=current_name, label=current)
        elif current is None:
            pass
        else:

            def process_child(child: Tree.Child):
                if child is None:
                    return

                if isinstance(child, Tree):
                    child_count = internal_node_count
                else:
                    child_count = leaf_node_count

                child_name = make_name(child_count)
                nodes.append((child_name, child))

                graph.node(child_name, label=f"r{child_name}")
                graph.edge(current_name, child_name)

            process_child(current.left)
            process_child(current.center)
            process_child(current.right)

    graph.render(view=True)


def print_parse_tree():
    result = parse_tree("(a+b)*abb")
    assert result is not None
    tree, remainder = result
    assert len(remainder) == 0
    print_tree(tree)


def print_all():
    actions = ["together", "union", "concat"]

    for action in actions:
        globals()[f"print_{action}"]()
        input()


if __name__ == "__main__":
    from .automata import Automata

    import sys

    args = sys.argv

    method_suffix = args[1]

    method = globals().get(
        f"print_{method_suffix}",
        lambda: print("no method defined. Check the parameter you passed"),
    )

    method()
