class Bet:
    def __init__(self, fixture, result, odds, stake):
        self.fixture = fixture
        self.result = result
        self.odds = odds
        self.stake = stake

    def won(self):
        return self.fixture.ftr == self.result

    def get_return(self):
        if self.won():
            return self.stake * self.odds
        else:
            return -self.stake