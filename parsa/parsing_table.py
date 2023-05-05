from .production import Production

Terminal = str
NonTerminal = str


class ParsingTable:
    matrix: dict[NonTerminal, dict[Terminal, Production]]
