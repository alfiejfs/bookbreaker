from models import Table, Fixture, Bet
from strategy import Strategy

class AlwaysHome(Strategy):
    
    def __init__(self, table: Table, amount: float):
        Strategy.__init__(self, table)
        self.amount = amount

    def handle_fixture(self, fixture: Fixture) -> Bet:
        return Bet(fixture, 'H', fixture.b365h, self.amount)