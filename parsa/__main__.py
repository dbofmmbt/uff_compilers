from pathlib import Path
import sys
from .look_ahead_table import END, look_ahead_table


def is_terminal(x):
    return look_ahead_table.get(x) == None


def error():
    raise Exception()


stack = [END, "Function"]


if len(sys.argv) > 1:
    print(f"getting tokens from file {sys.argv[1]}")
    tokens = eval(Path(sys.argv[1]).read_text().strip())
else:
    tokens: list[str] = eval(input("getting tokens from stdin"))


tokens.append(END)

position = 0

while (top := stack[-1]) != END:
    current_token = tokens[position]
    if top == current_token:
        stack.pop()
        position += 1
    elif is_terminal(top):
        error()
    else:
        next_rule = look_ahead_table[top].get(current_token)
        if next_rule is None:
            error()
        else:
            if next_rule == ["epsilon"]:
                stack.pop()
                continue

            # TODO output the production??
            print(f"{top} -> {' '.join(next_rule)}")

            stack.pop()
            for el in next_rule[::-1]:
                stack.append(el)
