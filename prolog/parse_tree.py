from dataclasses import dataclass
from typing import Self, Tuple


@dataclass
class Tree:
    Child = Self | None

    left: Child = None
    center: Child = None
    right: Child = None
    value: str | None = None


def concat(a: Tree.Child, b: Tree.Child) -> Tree:
    return Tree(left=a, center=None, right=b)


def parse_tree(regular_expression: str) -> Tuple[Tree, str] | None:
    current_tree, current_input = initial_tree(regular_expression)

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

                current_tree = concat(
                    current_tree, Tree(Tree(value=left), center, Tree(value=right))
                )
                current_input = remainder[1:]
            case "+":
                result = parse_tree(tail)
                assert result is not None, "operator '+' must have right operand"
                right_operand, remainder = result

                current_tree = Tree(
                    left=current_tree, center=Tree(value="+"), right=right_operand
                )
                current_input = remainder
            case "*":
                current_tree = concat(current_tree, Tree(value="*"))
                current_input = tail
            case ")":
                return current_tree, current_input
            case other:
                current_tree = concat(current_tree, Tree(value=other))
                current_input = tail

    return current_tree, ""


def initial_tree(regular_expression: str) -> Tuple[Tree, str]:
    head, tail = regular_expression[0:1], regular_expression[1:]

    match head:
        case "(":
            result = parse_tree(tail)
            assert result is not None, "missing center of ( expression"
            sub_tree, remainder = result
            assert remainder[0:1] == ")", "missing right paren"
            return (
                Tree(left=Tree(value="("), center=sub_tree, right=Tree(value=")")),
                remainder[1:],
            )
        case "+", "*", "", ")":
            raise Exception("not a valid regex")
        case other:
            return Tree(value=other), tail
