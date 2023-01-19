from models import Table
from datetime import timedelta

class MatchRunner:

    def __init__(self, table: Table):
        self.table = table
        self.datetime = None

    def advance_days(self, days):
        date = self.table.fixtures_to_play[0].datetime
        
        end_date = (date + timedelta(days = days)).date()
        
        while self.table.has_next_fixture() and self.table.get_next_fixture().datetime.date() < end_date:
            self.table.play_next_fixture()

    def can_run(self):
        return self.table.has_next_fixture()

    def run(self):
        self.advance_fixtures(1)

    def advance_fixtures(self, count):
        for _ in range(count):
            if not self.table.has_next_fixture():
                break
            self.table.play_next_fixture()

    def advance_team_games_played(self, game_count):
        starting_games = {}
        for team in self.table.teams:
            starting_games[team] = team.played()
        
        while self.table.has_next_fixture() and len(starting_games) > 0:
            fixture = self.table.get_next_fixture()
            self.table.play_next_fixture()
            if fixture.home in starting_games and fixture.home.played() == starting_games[fixture.home] + game_count:
                del starting_games[fixture.home]
            if fixture.away in starting_games and fixture.away.played() == starting_games[fixture.away] + game_count:
                del starting_games[fixture.away]