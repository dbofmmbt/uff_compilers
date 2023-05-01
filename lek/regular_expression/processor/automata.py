from ...automata import Automata
from .base import Processor
from ...automata_operations import union, closure, concat, unit


class AutomataProcessor(Processor[Automata]):
    def __init__(self, category: str):
        def unit_with_category(char: str):
            automata = unit(char)

            for final in automata.final_states():
                final.category = category

            return automata

        super().__init__(
            union=union, concat=concat, closure=closure, unit=unit_with_category
        )
