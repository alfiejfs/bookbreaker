from matchmodels import Table, Fixture
from bet import Bet
from strategy import Strategy

"""
Waits for 10 games to be played between both teams,
then bets on any team in the top 6 to win
"""
class TopSix(Strategy):
    
    games_required = 10
    
    def __init__(self, table: Table, stake: float):
        Strategy.__init__(self, table)
        self.stake = stake

    def handle_fixture(self, fixture: Fixture) -> Bet:
        if fixture.home.played() < TopSix.games_required or fixture.away.played() < TopSix.games_required:
            return None
            
        home_pos = self.table.position_of(fixture.home)
        away_pos = self.table.position_of(fixture.away)

        if home_pos >= 6 and away_pos >= 6:
            return None
        
        result = 'H' if home_pos > away_pos else "A"
        odds = fixture.b365h if result == 'H' else fixture.b365a
        return Bet(fixture, result, odds, self.stake)