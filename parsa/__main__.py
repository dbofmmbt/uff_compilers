from pathlib import Path
import sys

from .stack import Stack

from .dot import print_ast

from .ast import Tree
from .look_ahead_table import END, look_ahead_table, grammar


def is_terminal(x):
    return look_ahead_table.get(x) == None


def error():
    raise Exception()


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
    def parse(self, stream: TokenStream) -> Tree:
        first_rule = "Function"
        self.tree = Tree(first_rule)
        self.stack = Stack(END, first_rule)
        self.stream = stream

        while self.stack.top() != END and self.stream.next() != END:
            self.evaluate_next()

        if self.stack.top() == self.stream.next():
            print("GG")
        else:
            error()

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
            return error()

        next_rule = look_ahead_table[self.stack.top()].get(self.stream.next())
        if next_rule is None:
            return error()

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


tree = Parser().parse(TokenStream(tokens))

print_ast(tree)
