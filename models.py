class Table:
   
    def __init__(self, teams, fixtures_to_play):
        self.teams = teams
        self.fixtures_to_play = fixtures_to_play
        self.fixtures_played = []

        sort_teams()
        reorder_fixtures()

    @staticmethod
    def load_data_from_file(file):
        teams = {}
        fixtures = []
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

    def __cmp__(self, other):
        if other == None or not isinstance(other, Team):
            return 1

        if self.points() > other.points():
            return 1
        elif other.points() > self.points():
            return -1
        
        if self.gd() > other.gd():
            return 1
        elif other.gd() > self.gf():
            return -1

        if self.gf > other.gf:
            return 1
        elif other.gf > self.gf:
            return -1

        # Technical rules here are to do head to head points, then away goals in head to head, but I am too lazy to care.
        return self.name.__cmp__(other.name)

class Match:
    def __init__(self, div, date, time, home, away, fthg, ftag, ftr, hthg, htag, b365h, b365d, b365a):
        self.div = div
        self.date = date
        self.time = time
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

    def __cmp__(self, obj):
        if obj == None or not isinstance(obj, Team):
            return 1