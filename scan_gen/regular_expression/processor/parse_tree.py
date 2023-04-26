from .base import Processor
from ..literals import Literals
from ...parse_tree import Tree


def concat(a: Tree.Child, b: Tree.Child) -> Tree:
    return Tree(left=a, center=None, right=b)


def unit(char: str) -> Tree:
    return Tree(value=char)


def union(a: Tree, b: Tree) -> Tree:
    return Tree(
        left=a,
        center=unit(Literals.UNION),
        right=b,
    )


def closure(a: Tree) -> Tree:
    return concat(a, unit(Literals.CLOSURE))


class ParseTreeProcessor(Processor):
    def __init__(self):
        super().__init__(union=union, concat=concat, closure=closure, unit=unit)
