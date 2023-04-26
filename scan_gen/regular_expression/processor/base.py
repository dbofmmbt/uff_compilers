from typing import Callable, Generic, Tuple, TypeVar

from ..literals import Literals


T = TypeVar("T")


class Processor(Generic[T]):
    def __init__(
        self,
        unit: Callable[[str], T],
        union: Callable[[T, T], T],
        closure: Callable[[T], T],
        concat: Callable[[T, T], T],
    ):
        self.unit = unit
        self.union = union
        self.closure = closure
        self.concat = concat

    def process(self, regular_expression: str) -> Tuple[T, str]:
        current_state, current_expression = self.process_first(regular_expression)

        while True:
            head, tail = current_expression[0:1], current_expression[1:]

            match head:
                case "":
                    break
                case Literals.LEFT_PAREN:
                    tree, remainder = self.process_paren(current_expression)

                    current_state = self.concat(current_state, tree)
                    current_expression = remainder
                case Literals.UNION:
                    right_operand, remainder = self.process_first(tail)

                    current_state = self.union(current_state, right_operand)
                    current_expression = remainder
                case Literals.CLOSURE:
                    current_state = self.closure(current_state)
                    current_expression = tail
                case Literals.RIGHT_PAREN:
                    return current_state, current_expression
                case other:
                    current_state = self.concat(current_state, self.unit(other))
                    current_expression = tail

        return current_state, ""

    def process_paren(self, regular_expression: str) -> Tuple[T, str]:
        head, tail = regular_expression[0:1], regular_expression[1:]

        assert head == Literals.LEFT_PAREN

        center, remainder = self.process(tail)

        assert remainder[0:1] == Literals.RIGHT_PAREN, "missing right paren"

        return (
            center,
            remainder[1:],
        )

    def process_first(self, regular_expression: str) -> Tuple[T, str]:
        head, tail = regular_expression[0:1], regular_expression[1:]

        match head:
            case Literals.LEFT_PAREN:
                return self.process_paren(regular_expression)
            case Literals.UNION, Literals.CLOSURE, "", Literals.RIGHT_PAREN:
                raise Exception("not a valid regex")
            case other:
                return self.unit(other), tail
