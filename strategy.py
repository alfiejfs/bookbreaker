from abc import ABC, abstractmethod
from matchmodels import Table, Fixture
from bet import Bet

class Strategy(ABC):

    def __init__(self, table: Table):
        self.table = table
        self.total_stake = 0

    def calculate_fixture(self, fixture: Fixture) -> Bet:
        bet = self.handle_fixture(fixture)
        if bet is not None:
            self.total_stake += bet.stake
        return bet

    @abstractmethod
    def handle_fixture(self, fixture: Fixture) -> Bet:
        pass