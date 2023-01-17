from functools import total_ordering
from datetime import datetime

class Table:
    def __init__(self, teams, fixtures_to_play):
        self.teams = teams
        self.fixtures_to_play = fixtures_to_play
        self.fixtures_played = []

        self.sort_teams()
        self.reorder_fixtures()

    def sort_teams(self):
        self.teams = sorted(self.teams)
   
    def reorder_fixtures(self):
        self.fixtures_to_play = sorted(self.fixtures_to_play)

    @staticmethod
    def load_data_from_file(file):
        teams = {}
        fixtures = []
        next(file) # skipping first line
        for line in file:
            data = line.split(",")
            div = data[0]
            date = data[1]
            time = data[2]
            
            if data[3] not in teams:
                teams[data[3]] = Team(data[3])
            home = teams[data[3]]
            
            if data[4] not in teams:
                teams[data[4]] = Team(data[4])
            away = teams[data[4]]

            fthg = data[5]
            ftag = data[6]
            ftr = data[7]
            hthg = data[8]
            htag = data[9]
            b365h = data[24]
            b365d = data[25]
            b365a = data[26]

            fixtures.append(Match(div, date, time, home, away, fthg, ftag, ftr, hthg, htag, b365h, b365d, b365a))

        return Table(list(teams.values()), fixtures)

@total_ordering
class Team:
    def __init__(self, name):
        self.name = name
        self.won = 0
        self.lost = 0
        self.drawn = 0
        self.gf = 0
        self.ga = 0

    def points(self):
        return self.won * 3 + self.drawn

    def gd(self):
        return self.gf - self.ga

    def __repr__(self):
        return (
            f"Team{{name: {self.name}, points: {self.points()}, won: {self.won}, lost: {self.lost}, drawn: {self.drawn}, " 
            f"gd: {self.gd()}, gf: {self.gf}, ga: {self.ga}}}"
        )

    def __lt__(self, other):
        if other == None or not isinstance(other, Team):
            return False
      
        if self.points() == other.points():
            if self.gd() == other.gd():
                if self.gf == other.gf:
                    return self.name < other.name
                return self.gf > other.gf
            return self.gd() > other.gd()
        return self.points() > other.points()
    
    def __eq__(self, other):
        if other == None or not isinstance(other, Team):
            return False

        return self.points() == other.points() and self.gd() == other.gd() and self.gf == other.gf and self.name == other.name

@total_ordering
class Match:
    def __init__(self, div, date, time, home, away, fthg, ftag, ftr, hthg, htag, b365h, b365d, b365a):
        self.div = div
        self.datetime = datetime.strptime(date + " " + time, "%d/%m/%Y %H:%M")
        self.home = home
        self.away = away
        self.fthg = fthg
        self.ftag = ftag
        self.ftr = ftr
        self.hthg = hthg
        self.htag = htag
        self.b365h = b365h
        self.b365d = b365d
        self.b365a = b365a

    def __repr__(self):
        return (
            f"Match{{div: {self.div}, datetime: {self.datetime}, home: {self.home}, away: {self.away}, fthg: {self.fthg}, "
            f"ftag: {self.ftag}, ftr: {self.ftr}, hthg: {self.hthg}, htag: {self.htag}, b365h: {self.b365h}, b365d: {self.b365d}, "
            f"b36ga: {self.b365a}}}"
        )

    def __lt__(self, other):
        if other == None or not isinstance(other, Match):
            return False

    def __eq__(self, other):
        if other == None or not isinstance(other, Match):
            return False

        return self.div == other.div and self.datetime == other.datetime \
                and self.home == other.home and self.away == other.away \
                and self.fthg == other.fthg and self.ftag == other.ftag \
                and self.ftr == other.ftr and self.hthg == other.hthg \
                and self.htag == other.htag and self.b365h == other.b365h \
                and self.b365d == other.b365d and self.b365a == other.b365a
