from abc import ABC, abstractmethod
from models import Table, Fixture, Bet

class Strategy(ABC):

    def __init__(self, table: Table):
        self.table = table

    @abstractmethod
    def handle_fixture(self, fixture: Fixture) -> Bet:
        pass