# letra minuscula
from prolog.category import Category
from prolog import machines


def categories():
    return [
        Category(label="DOT", machine=machines.dot()),
        Category(label="COMMA", machine=machines.comma()),
        Category(label="TWO_DOTS_SLASH", machine=machines.two_dots_dash()),
        Category(label="QUERY", machine=machines.query()),

        Category(label="LEFT_PAREN", machine=machines.left_paren()),
        Category(label="RIGHT_PAREN", machine=machines.right_paren()),

        Category(label="ATOM", machine=machines.atom()),
        Category(label="VARIABLE", machine=machines.variable()),
        Category(label="NUMERAL", machine=machines.numeral()),
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
