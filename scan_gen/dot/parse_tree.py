from itertools import count

import graphviz
from ..parse_tree import Tree


class TreeInfo:
    internal_node_count = count()
    leaf_node_count = count()

    def __init__(self, tree: Tree):
        self.tree = tree

        if tree.value is None:
            self.name = f"r{next(self.internal_node_count)}"
            self.label = self.name
        else:
            self.name = str(next(self.leaf_node_count))
            self.label = tree.value

    def graph_node(self) -> dict:
        return {"name": self.name, "label": self.label}


def print_tree(root: Tree):
    graph = graphviz.Graph()

    root_info = TreeInfo(root)
    graph.node(**root_info.graph_node())
    nodes = [root_info]

    while nodes:
        current = nodes.pop(0)

        def process_child(child: Tree.Child):
            if child is None:
                return

            child_info = TreeInfo(child)

            nodes.append(child_info)

            graph.node(**child_info.graph_node())
            graph.edge(current.name, child_info.name)

        process_child(current.tree.left)
        process_child(current.tree.center)
        process_child(current.tree.right)

    graph.render(view=True)
