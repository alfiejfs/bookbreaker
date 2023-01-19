from matchmodels import Table, Fixture
from bet import Bet
from strategy import Strategy

"""
Waits for 5 games to be played.
Bets £1 on the team with more points per point of difference between the team
if and only if exactly one team in the fixture is in the top 6
"""
class PoundPerPointTopSix(Strategy):
    
    games_required = 5

    def __init__(self, table: Table, stake: float):
        Strategy.__init__(self, table)
        self.stake = stake

    def handle_fixture(self, fixture: Fixture) -> Bet:
        if fixture.home.played() < PoundPerPointTopSix.games_required or fixture.away.played() < PoundPerPointTopSix.games_required:
            return None
    
        home_points = fixture.home.points()
        away_points = fixture.away.points()
        home_pos = self.table.position_of(fixture.home)
        away_pos = self.table.position_of(fixture.away)

        if (home_pos < 6 and away_pos < 6) or (home_pos >= 6 and away_pos >= 6) or home_points == away_points:
            return None
        elif home_points > away_points:
            return Bet(fixture, 'H', fixture.b365h, home_points - away_points)
        else:
            return Bet(fixture, 'A', fixture.b365a, away_points - home_points)