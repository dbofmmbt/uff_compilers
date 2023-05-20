from typing import Tuple
from pathlib import Path
import sys
from typing import Self

from .stack import Stack

from .dot import print_ast

from .ast import Tree
from .look_ahead_table import END, FOLLOW_KEY, look_ahead_table, grammar


def is_terminal(x):
    return look_ahead_table.get(x) == None


TokenInput = Tuple[str, str, int]

if len(sys.argv) > 1:
    print(f"getting tokens from file {sys.argv[1]}")
    tokens = eval(Path(sys.argv[1]).read_text().strip())
else:
    tokens: list[TokenInput] = eval(input("getting tokens from stdin"))


tokens.append((END, END, 0))


class TokenStream:
    def __init__(self, tokens: list[TokenInput]) -> None:
        self.tokens = tokens
        self.position = -1

    def next(self, by=1) -> TokenInput:
        return self.tokens[self.position + by]

    def advance(self):
        self.position += 1

    def copy(self) -> Self:
        stream = TokenStream(self.tokens)
        stream.position = self.position
        return stream


class Parser:
    def __init__(self, stream: TokenStream, fail_fast=False) -> None:
        self.errors = []
        first_rule = "Function"
        self.tree = Tree(first_rule)
        self.stack = Stack(END, first_rule)
        self.stream = stream
        self.fail_fast = fail_fast
        self.backtrack_failed_recently = False

    def parse(self) -> Tree | list[str]:
        while self.stack.top() != END and self.stream.next()[0] != END:
            self.evaluate_next()

        while self.tree.ancestor:
            self.tree = self.tree.ancestor

        if self.stack.top() == self.stream.next()[0] and not self.errors:
            print("GG")
        else:
            return self.errors

        return self.tree

    def evaluate_next(self):
        if self.stack.top() == self.stream.next()[0]:
            self.stack.pop()
            self.stream.advance()
            self.tree = self.tree.next_sibling() or self.tree
            self.backtrack_failed_recently = False
            return

        if is_terminal(self.stack.top()):
            if not self.backtrack_failed_recently:
                self.error(
                    f"On line {self.stream.next()[2]} input `{self.stream.next()[0]}` != stack `{self.stack.top()}`"
                )
            self.stream.advance()
            return

        next_rule = look_ahead_table[self.stack.top()].get(self.stream.next()[0])

        if next_rule is None:
            expected_symbols = [
                symbol
                for symbol in look_ahead_table[self.stack.top()].keys()
                if symbol != FOLLOW_KEY
            ]

            self.error(
                f"On Line {self.stream.next()[2]} found `{self.stream.next()[0]}`, expected one of {{ {' '.join(expected_symbols)} }}"
            )

            entry = look_ahead_table.get(self.stack.top())
            if entry and self.stream.next()[0] in entry[FOLLOW_KEY]:
                self.stack.pop()
            else:
                self.stream.advance()

            return

        if next_rule == ["epsilon"]:
            self.stack.pop()

            self.tree.child("ε")

            self.tree = self.tree.next_sibling() or self.tree

            return

        sub_parser = None
        more_than_one_rule = isinstance(next_rule[0], list)
        if more_than_one_rule:
            errors = None
            self.stack.pop()
            for rule in next_rule:
                sub_parser = Parser(self.stream.copy(), fail_fast=True)
                sub_parser.stack = Stack(END)
                sub_parser.tree = self.tree.copy()

                for el in rule[::-1]:
                    sub_parser.stack.push(el)

                for el in rule:
                    sub_parser.tree.child(el)
                sub_parser.tree = sub_parser.tree.children[0]

                result = sub_parser.parse()

                if sub_parser.stack.top() == END and not sub_parser.errors:
                    self.stream = sub_parser.stream
                    self.tree.children = sub_parser.tree.children
                    self.tree = self.tree.next_sibling() or self.tree
                    return
                else:
                    assert isinstance(result, list)
                    errors = result
            if errors is not None:
                assert sub_parser
                self.stream = sub_parser.stream
                self.errors += errors
                self.backtrack_failed_recently = True
                return

        self.stack.pop()
        for el in next_rule[::-1]:
            self.stack.push(el)

        for rule in next_rule:
            self.tree.child(rule)
        self.tree = self.tree.children[0]

    def error(self, error):
        self.errors.append(error)
        if self.fail_fast:
            self.stack.push(END)


result = Parser(TokenStream(tokens)).parse()

if type(result) is Tree:
    print_ast(result)

    ident = 0
    for leave in result.leaves():
        match leave.content:
            case "{":
                ident += 4
            case "}":
                ident -= 4

        if leave.content in "}":
            print("\n" + " " * ident, end="")

        print(leave.content, end=" ")

        if leave.content in "{;":
            print("\n" + " " * ident, end="")
    print()
elif type(result) is list:
    print("\nErrors found by the parser:")
    for error in result:
        print(f"    - {error}")
