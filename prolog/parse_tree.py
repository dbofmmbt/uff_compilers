from dataclasses import dataclass
from typing import Self, Tuple


@dataclass
class Tree:
    Child = Self | str | None

    left: Child
    center: Child
    right: Child


def concat(a, b) -> Tree:
    return Tree(left=a, center=None, right=b)


def parse_tree(regular_expression: str) -> Tuple[Tree, str] | None:
    current_tree = None

    current_input = regular_expression
    while True:
        head, tail = current_input[0:1], current_input[1:]

        match head:
            case "":
                break
            case "(":
                left = head
                result = parse_tree(tail)
                assert result is not None, "missing center of ( expression"

                center, remainder = result
                assert remainder[0:1] == ")", "missing right paren"
                right = ")"

                current_tree = concat(current_tree, Tree(left, center, right))
                current_input = remainder[1:]
            case "+":
                result = parse_tree(tail)
                assert result is not None, "operator '+' must have right operand"
                right_operand, remainder = result

                current_tree = Tree(left=current_tree, center="+", right=right_operand)
                current_input = remainder
            case "*":
                current_tree = concat(current_tree, "*")
                current_input = tail
            case ")":
                assert current_tree is not None
                return current_tree, current_input
            case other:
                current_tree = concat(current_tree, other)
                current_input = tail

    assert current_tree is not None
    return current_tree, ""