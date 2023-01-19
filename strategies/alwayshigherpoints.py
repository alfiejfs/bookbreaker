from matchmodels import Table, Fixture
from bet import Bet
from strategy import Strategy

class AlwaysHigherPoints(Strategy):
    
    def __init__(self, table: Table, stake: float):
        Strategy.__init__(self, table)
        self.stake = stake

    def handle_fixture(self, fixture: Fixture) -> Bet:
        home_points = fixture.home.points()
        away_points = fixture.away.points()
        if home_points > away_points:
            return Bet(fixture, 'H', fixture.b365h, self.stake)
        elif away_points > home_points:
            return Bet(fixture, 'A', fixture.b365a, self.stake)