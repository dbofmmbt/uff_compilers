class Stack:
    def __init__(self, *initial) -> None:
        self.items = [*initial]

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[-1]
