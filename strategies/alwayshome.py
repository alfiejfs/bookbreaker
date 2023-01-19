from matchmodels import Table, Fixture
from bet import Bet
from strategy import Strategy

class AlwaysHome(Strategy):
    
    def __init__(self, table: Table, stake: float):
        Strategy.__init__(self, table)
        self.stake = stake

    def handle_fixture(self, fixture: Fixture) -> Bet:
        return Bet(fixture, 'H', fixture.b365h, self.stake)