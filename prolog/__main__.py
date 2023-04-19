# letra minuscula
from prolog import machines


def categories():
    return [
        ("DOT", machines.dot()),
        ("COMMA", machines.comma()),
        ("TWO_DOTS_SLASH", machines.two_dots_dash()),
        ("QUERY", machines.query()),
        ("LEFT_PAREN", machines.left_paren()),
        ("RIGHT_PAREN", machines.right_paren()),
        ("ATOM", machines.atom()),
        ("VARIABLE", machines.variable()),
        ("NUMERAL", machines.numeral()),
    ]


def read_program(file_name: str):
    output = []
    with open(file_name, "r") as f:
        program = f.read()

    # reset state
    prolog = categories()
    word = ""

    for char in program:
        match char:
            case "\n", " ":
                category.machine = category.machine.apply_input(char)
                if category.machine.is_final:
                    output.append((category.label, word))

                # reset state
                prolog = categories()
                word = ""
                continue

        word += char

        for category in prolog:
            category.machine = category.machine.apply_input(char)
            if category.machine.is_final:
                output.append((category.label, word))
                # reset state
                prolog = categories()
                word = ""
                break

    return output


print(read_program("input.txt"))
