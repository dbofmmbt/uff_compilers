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
FOLLOW_KEY = "__follow"
look_ahead_table = {
    "Function": {"int": 0, "float": 0, FOLLOW_KEY: set()},
    "Type": {"int": 0, "float": 1, FOLLOW_KEY: set(["identifier"])},
    "ArgList": {"int": 0, "float": 0, FOLLOW_KEY: set([")"])},
    "CompoundStmt": {
        "{": 0,
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                "$",
                ";",
                "int",
                "float",
                "for",
                "while",
                "if",
                "else",
                "{",
                "}",
                "+",
                "-",
                "number",
            ]
        ),
    },
    "Arg": {"int": 0, "float": 0, FOLLOW_KEY: set([")" ","])},
    "ArgList2": {",": 0, ")": 1, FOLLOW_KEY: set([")" ","])},
    "Declaration": {
        "int": 0,
        "float": 0,
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                ";",
                "int",
                "float",
                "for",
                "while",
                "if",
                "else",
                "{",
                "}",
                "+",
                "-",
                "number",
            ]
        ),
    },
    "IdentList": {"identifier": 0, FOLLOW_KEY: set([";"])},
    "IdentList2": {",": 0, ";": 1, FOLLOW_KEY: set([";"])},
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
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                ";",
                "int",
                "float",
                "for",
                "while",
                "if",
                "else",
                "{",
                "}",
                "+",
                "-",
                "number",
            ]
        ),
    },
    "ForStmt": {
        "for": 0,
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                ";",
                "int",
                "float",
                "for",
                "while",
                "if",
                "else",
                "{",
                "}",
                "+",
                "-",
                "number",
            ]
        ),
    },
    "WhileStmt": {
        "while": 0,
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                ";",
                "int",
                "float",
                "for",
                "while",
                "if",
                "else",
                "{",
                "}",
                "+",
                "-",
                "number",
            ]
        ),
    },
    "Expr": {
        "identifier": [0, 1],
        "(": 1,
        "+": 1,
        "-": 1,
        "number": 1,
        FOLLOW_KEY: set([")", ";"]),
    },
    "IfStmt": {
        "if": [0, 1],
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                ";",
                "int",
                "float",
                "for",
                "while",
                "if",
                "else",
                "{",
                "}",
                "+",
                "-",
                "number",
            ]
        ),
    },
    "OptExpr": {
        "identifier": 0,
        "(": 0,
        "+": 0,
        "-": 0,
        "number": 0,
        ")": 1,
        ";": 1,
        FOLLOW_KEY: set([")", ";"]),
    },
    "ElsePart": {
        "else": 0,
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                ";",
                "int",
                "float",
                "for",
                "while",
                "if",
                "else",
                "{",
                "}",
                "+",
                "-",
                "number",
            ]
        ),
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
        FOLLOW_KEY: set(["}"]),
    },
    "Rvalue": {
        "identifier": 0,
        "(": 0,
        "+": 0,
        "-": 0,
        "number": 0,
        FOLLOW_KEY: set([")", ";"]),
    },
    "Mag": {
        "identifier": 0,
        "(": 0,
        "+": 0,
        "-": 0,
        "number": 0,
        FOLLOW_KEY: set([")", ";", "==", "<", ">", "<=", ">=", "!="]),
    },
    "Rvalue2": {
        "==": 0,
        "<": 0,
        ">": 0,
        "<=": 0,
        ">=": 0,
        "!=": 0,
        ")": 1,
        ";": 1,
        FOLLOW_KEY: set([")", ";"]),
    },
    "Compare": {
        "==": 0,
        "<": 1,
        ">": 2,
        "<=": 3,
        ">=": 4,
        "!=": 5,
        FOLLOW_KEY: set(
            [
                "identifier",
                "(",
                "+",
                "-",
                "number",
            ]
        ),
    },
    "Term": {
        "identifier": 0,
        "(": 0,
        "+": 0,
        "-": 0,
        "number": 0,
        FOLLOW_KEY: set([")", ";", "==", "<", ">", "<=", ">=", "!=", "+", "-"]),
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
        FOLLOW_KEY: set(
            [
                ")",
                ";",
                "==",
                "<",
                ">",
                "<=",
                ">=",
                "!=",
            ]
        ),
    },
    "Factor": {
        "(": 0,
        "-": 1,
        "+": 2,
        "identifier": 3,
        "number": 4,
        FOLLOW_KEY: set(
            [
                ")",
                ";",
                "==",
                "<",
                ">",
                "<=",
                ">=",
                "!=",
                "+",
                "-",
                "*",
                "/",
            ]
        ),
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
        FOLLOW_KEY: set([")", ";", "==", "<", ">", "<=", ">=", "!=", "+", "-"]),
    },
}

for non_terminal, terminals in look_ahead_table.items():
    for terminal, rule in terminals.items():
        if type(rule) is int:
            look_ahead_table[non_terminal][terminal] = grammar[non_terminal][rule]  # type: ignore
        elif type(rule) is list:
            look_ahead_table[non_terminal][terminal] = [
                grammar[non_terminal][r] for r in rule
            ]

look_ahead_table = typing.cast(dict[str, dict[str, list[str]]], look_ahead_table)

if __name__ == "__main__":
    print(look_ahead_table)
