from pathlib import Path
import sys

from .stack import Stack

from .dot import print_ast

from .ast import Tree
from .look_ahead_table import END, FOLLOW_KEY, look_ahead_table, grammar


def is_terminal(x):
    return look_ahead_table.get(x) == None


if len(sys.argv) > 1:
    print(f"getting tokens from file {sys.argv[1]}")
    tokens = eval(Path(sys.argv[1]).read_text().strip())
else:
    tokens: list[str] = eval(input("getting tokens from stdin"))


tokens.append(END)


class TokenStream:
    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.position = -1

    def next(self, by=1) -> str:
        return self.tokens[self.position + by]

    def advance(self):
        self.position += 1


class Parser:
    def __init__(self) -> None:
        self.errors = []

    def parse(self, stream: TokenStream) -> Tree | list[str]:
        first_rule = "Function"
        self.tree = Tree(first_rule)
        self.stack = Stack(END, first_rule)
        self.stream = stream

        while self.stack.top() != END and self.stream.next() != END:
            self.evaluate_next()

        if self.stack.top() == self.stream.next() and not self.errors:
            print("GG")
        else:
            return self.errors

        while self.tree.ancestor:
            self.tree = self.tree.ancestor

        return self.tree

    def evaluate_next(self):
        if self.stack.top() == self.stream.next():
            self.stack.pop()
            self.stream.advance()
            self.tree = self.tree.next_sibling() or self.tree
            return

        if is_terminal(self.stack.top()):
            self.error(f"input `{self.stream.next()}` != stack `{self.stack.top()}`")
            self.stream.advance()
            return

        next_rule = look_ahead_table[self.stack.top()].get(self.stream.next())
        if next_rule is None:
            self.error(
                f"missing rule for stack `{self.stack.top()}` input `{self.stream.next()}`)"
            )

            if self.stream.next() in look_ahead_table[self.stack.top()][FOLLOW_KEY]:
                self.stack.pop()
            else:
                self.stream.advance()

            return

        if next_rule == ["epsilon"]:
            self.stack.pop()

            if self.tree.ancestor and not self.tree.children:
                # Remove rule that turned out to be empty from ancestor
                self.tree.ancestor.children.remove(self.tree)

            self.tree = self.tree.next_sibling() or self.tree

            return

        next_rule = self.expr_aware(next_rule)

        self.stack.pop()
        for el in next_rule[::-1]:
            self.stack.push(el)

        for rule in next_rule:
            self.tree.child(rule)
        self.tree = self.tree.children[0]

    def expr_aware(self, rule):
        if self.stack.top() == "Expr" and self.stream.next(by=2) != "=":
            return grammar["Expr"][1]

        return rule

    def error(self, error):
        self.errors.append(error)


result = Parser().parse(TokenStream(tokens))

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
