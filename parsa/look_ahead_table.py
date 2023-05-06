import typing


with open("parsa/mini_c_grammar/ready_for_parsa.txt", "r") as f:
    rules = (l for l in f.readlines() if l.strip() != "")

grammar: dict[str, list[list[str]]] = {}

for rule in rules:
    left, right = rule.split("->")
    left, right = left.strip(), right.strip().split()

    non_terminal_rules = grammar.get(left)

    if not non_terminal_rules:
        grammar[left] = [right]
    else:
        non_terminal_rules.append(right)

END = "$"

look_ahead_table = {
    "Function": {"int": 0, "float": 0},
    "Type": {"int": 0, "float": 1},
    "ArgList": {"int": 0, "float": 0},
    "CompoundStmt": {"{": 0},
    "Arg": {"int": 0, "float": 0},
    "ArgList2": {",": 0, ")": 1},
    "Declaration": {"int": 0, "float": 0},
    "IdentList": {"identifier": 0},
    "IdentList2": {",": 0, ";": 1},
    "Stmt": {
        "identifier": 2,
        "(": 2,
        ";": 6,
        "int": 5,
        "float": 5,
        "for": 0,
        "while": 1,
        "if": 3,
        "{": 4,
        "+": 2,
        "-": 2,
        "number": 2,
    },
    "ForStmt": {"for": 0},
    "WhileStmt": {"while": 0},
    "Expr": {
        # Checar com o professor oq fazer, pq identifier pode estar nas 2 regras
        "identifier": 0,
        "(": 1,
        "+": 1,
        "-": 1,
        "number": 1,
    },
    "IfStmt": {"if": 0},
    "OptExpr": {
        "identifier": 0,
        "(": 0,
        "+": 0,
        "-": 0,
        "number": 0,
        ")": 1,
        ";": 1,
    },
    "ElsePart": {
        "else": 0,
        "identifier": 1,
        "(": 1,
        ";": 1,
        "int": 1,
        "float": 1,
        "for": 1,
        "while": 1,
        "if": 1,
        "else": 1,
        "{": 1,
        "}": 1,
        "+": 1,
        "-": 1,
        "number": 1,
    },
    "StmtList": {
        "identifier": 0,
        "(": 0,
        ";": 0,
        "int": 0,
        "float": 0,
        "for": 0,
        "while": 0,
        "if": 0,
        "{": 0,
        "+": 0,
        "-": 0,
        "number": 0,
        "}": 1,
    },
    "Rvalue": {"identifier": 0, "(": 0, "+": 0, "-": 0, "number": 0},
    "Mag": {
        "identifier": 0,
        "(": 0,
        "+": 0,
        "-": 0,
        "number": 0,
    },
    "Rvalue2": {"==": 0, "<": 0, ">": 0, "<=": 0, ">=": 0, "!=": 0, ")": 1, ";": 1},
    "Compare": {
        "==": 0,
        "<": 1,
        ">": 2,
        "<=": 3,
        ">=": 4,
        "!=": 5,
    },
    "Term": {
        "identifier": 0,
        "(": 0,
        "+": 0,
        "-": 0,
        "number": 0,
    },
    "Mag2": {
        "+": 0,
        "-": 1,
        ")": 2,
        ";": 2,
        "==": 2,
        "<": 2,
        ">": 2,
        "<=": 2,
        ">=": 2,
        "!=": 2,
    },
    "Factor": {
        "(": 0,
        "-": 1,
        "+": 2,
        "identifier": 3,
        "number": 4,
    },
    "Term2": {
        "*": 0,
        "/": 1,
        ")": 2,
        ";": 2,
        "==": 2,
        "<": 2,
        ">": 2,
        "<=": 2,
        ">=": 2,
        "!=": 2,
        "+": 2,
        "-": 2,
    },
}

for non_terminal, terminals in look_ahead_table.items():
    for terminal, rule in terminals.items():
        look_ahead_table[non_terminal][terminal] = grammar[non_terminal][rule]  # type: ignore

look_ahead_table = typing.cast(dict[str, dict[str, list[str]]], look_ahead_table)

if __name__ == "__main__":
    print(look_ahead_table)
