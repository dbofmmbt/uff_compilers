import graphviz
from prolog import machines

from prolog.machines import two_dots_dash
from prolog.regular_expression import union
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


def print_automata(automata: Automata):
    dot = graphviz.Digraph("Automata")

    for id, state in automata.states.items():
        border_count = 2 if state.is_final else 1

        dot.node(set_to_str(id), peripheries=str(border_count))

        for transition in state.transitions:
            dot.edge(
                set_to_str(id),
                set_to_str(transition.destination),
                transition.trigger,
            )

    dot.render(view=True)


def set_to_str(a):
    return str(set(a))


if __name__ == "__main__":
    from .automata import Automata

    automata = Automata()

    state0 = automata.add_state()
    state1 = automata.add_state(category="DOT")

    automata.add_transition(state0.name, state1.name, ".")
    other = two_dots_dash()

    print_automata(union(automata, other))
