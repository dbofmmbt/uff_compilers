from typing import Iterator, Self


class Tree:
    ancestor: Self | None = None
    children: list[Self]
    content: str

    def __init__(self, content: str) -> None:
        self.children = []
        self.content = content

    def child(self, content: str) -> Self:
        child = Tree(content)
        child.ancestor = self

        self.children.append(child)

        return child

    def next_sibling(self) -> Self | None:
        if not self.ancestor:
            return None

        i = 0
        siblings = self.ancestor.children
        while i < len(siblings):
            if siblings[i] is self and i + 1 < len(siblings):
                return siblings[i + 1]
            i += 1

        return self.ancestor.next_sibling()

    def leaves(self) -> Iterator[Self]:
        if not self.children:
            yield self
            return
        
        for child in self.children:
            for leave in child.leaves():
                yield leave
