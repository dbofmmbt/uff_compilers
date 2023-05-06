import graphviz

from .ast import Tree
import uuid


def print_ast(tree: Tree):
    graph = graphviz.Digraph()
    populate_graph_with_ast(graph, tree, str(uuid.uuid4()))
    graph.render(view=True)


def populate_graph_with_ast(graph: graphviz.Digraph, tree: Tree, id, find_root=True):
    while find_root and tree.ancestor:
        tree = tree.ancestor

    graph.node(name=id, label=tree.content)

    for child in tree.children:
        child_id = str(uuid.uuid4())
        graph.edge(tail_name=id, head_name=child_id)

        if not child.children:
            graph.node(name=child_id, color="red")

        populate_graph_with_ast(graph, child, child_id, find_root=False)
