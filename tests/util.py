from lek.scanner import Scanner


def check(scanner: Scanner, source: str, expected: str):
    tokens = list(map(lambda t: (t.category, t.value), scanner.scan(source)))

    expected_tokens = []

    for line in filter(lambda l: l.strip() != "", expected.splitlines()):
        category, value = line.split()
        expected_tokens.append((category, value))

    assert tokens == expected_tokens
