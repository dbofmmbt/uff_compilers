from ..dot.automata import print_automata
from ..parse_tree import Tree, parse_tree
from ..automata import Automata


def convert(root: Tree) -> Automata:
    automata = Automata()

    nodes_to_register: list[Tree] = []
    nodes_to_visit = []

    def add_in_front(child: Tree.Child):
        if child is not None:
            nodes_to_register.insert(0, child)

    def add_children(parent: Tree):
        add_in_front(parent.right)
        add_in_front(parent.center)
        add_in_front(parent.left)

    add_children(root)

    while nodes_to_register:
        node = nodes_to_register.pop(0)

        if node.is_leaf:
            nodes_to_visit.append(node)
            continue

        add_children(node)

    print(list(map(lambda t: t.value, nodes_to_visit)))

    raise NotImplementedError()


if __name__ == "__main__":
    tree, _ = parse_tree("(a+b)*abb")
    automata = convert(tree)
    print_automata(automata)
