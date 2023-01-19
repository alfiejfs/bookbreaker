from matchmodels import Table, Fixture
from bet import Bet
from strategy import Strategy

"""
Waits for 10 games to be played.
Bets £1 on the team with more points per point of difference between the team
"""
class PoundPerPoint(Strategy):
    
    games_required = 10
    max_bet = 9999

    def __init__(self, table: Table, stake: float):
        Strategy.__init__(self, table)
        self.stake = stake

    def handle_fixture(self, fixture: Fixture) -> Bet:
        if fixture.home.played() < PoundPerPoint.games_required or fixture.away.played() < PoundPerPoint.games_required:
            return None
    
        home_points = fixture.home.points()
        away_points = fixture.away.points()

        if home_points == away_points:
            return None
        elif home_points > away_points:
            return Bet(fixture, 'H', fixture.b365h, min(home_points - away_points, PoundPerPoint.max_bet))
        else:
            return Bet(fixture, 'A', fixture.b365a, min(away_points - home_points, PoundPerPoint.max_bet))