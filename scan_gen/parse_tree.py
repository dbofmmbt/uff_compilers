from dataclasses import dataclass
from typing import Self, Tuple


class Literal:
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    CLOSURE = "*"
    UNION = "+"


@dataclass
class Tree:
    Child = Self | None

    left: Child = None
    center: Child = None
    right: Child = None
    value: str | None = None

    @property
    def is_leaf(self) -> bool:
        return self.value is not None


def concat(a: Tree.Child, b: Tree.Child) -> Tree:
    return Tree(left=a, center=None, right=b)


def parse_tree(regular_expression: str) -> Tuple[Tree, str]:
    current_tree, current_input = initial_tree(regular_expression)

    while True:
        head, tail = current_input[0:1], current_input[1:]

        match head:
            case "":
                break
            case Literal.LEFT_PAREN:
                tree, remainder = paren_tree(current_input)

                current_tree = concat(current_tree, tree)
                current_input = remainder
            case Literal.UNION:
                right_operand, remainder = initial_tree(tail)

                current_tree = Tree(
                    left=current_tree,
                    center=Tree(value=Literal.UNION),
                    right=right_operand,
                )
                current_input = remainder
            case Literal.CLOSURE:
                current_tree = concat(current_tree, Tree(value=Literal.CLOSURE))
                current_input = tail
            case Literal.RIGHT_PAREN:
                return current_tree, current_input
            case other:
                current_tree = concat(current_tree, Tree(value=other))
                current_input = tail

    return current_tree, ""


def paren_tree(regular_expression: str) -> Tuple[Tree, str]:
    head, tail = regular_expression[0:1], regular_expression[1:]

    assert head == Literal.LEFT_PAREN

    center, remainder = parse_tree(tail)

    assert remainder[0:1] == Literal.RIGHT_PAREN, "missing right paren"

    return (
        center,
        remainder[1:],
    )


def initial_tree(regular_expression: str) -> Tuple[Tree, str]:
    head, tail = regular_expression[0:1], regular_expression[1:]

    match head:
        case Literal.LEFT_PAREN:
            return paren_tree(regular_expression)
        case Literal.UNION, Literal.CLOSURE, "", Literal.RIGHT_PAREN:
            raise Exception("not a valid regex")
        case other:
            return Tree(value=other), tail
