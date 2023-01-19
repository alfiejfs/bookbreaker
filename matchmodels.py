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

    def position_of(self, team):
        self.sort_teams()
        return self.teams.index(team) 

    def play_next_fixture(self):
        fixture = self.fixtures_to_play[0]
        self.fixtures_to_play.remove(fixture)
        fixture.play()
        self.fixtures_played.append(fixture)

    def has_next_fixture(self):
        return len(self.fixtures_to_play) > 0
    
    def get_next_fixture(self):
        return self.fixtures_to_play[0]

    def show(self):
        self.sort_teams()

        print("Pos. Team | MP | W D L | GF GA GD | Pts")
        print("---------------------------------------")

        longest_name = 0
        for i in range(len(self.teams)):
            team = self.teams[i]
            value = len(team.name) + 2 + len(str(i + 1))
            if value > longest_name:
                longest_name = value

        for i in range(len(self.teams)):
            team = self.teams[i]
            display_name = f"{i + 1}. {team.name}"
            while len(display_name) < longest_name:
                display_name += " "
            print(f"{display_name} | {team.played()} | {team.won} {team.drawn} {team.lost} | {team.gf} {team.ga} {team.gd()} | {team.points()}")
            

    @staticmethod
    def load_data_from_file(file):
        teams = {}
        fixtures = []
        line = next(file) # skipping first line
        has_time = 'Time' in line
        for line in file:
            data = line.split(",")
            div = data[0]
            date = data[1]
            
            # Some data doesn't record the time. If not, all times will be 00:00
            index = 1
            time = "00:00"
            if has_time:
                index = 0
                time = data[2]
            
            if data[3 - index] not in teams:
                teams[data[3 - index]] = Team(data[3 - index], div)
            home = teams[data[3 - index]]
            
            if data[4 - index] not in teams:
                teams[data[4 - index]] = Team(data[4 - index], div)
            away = teams[data[4 - index]]

            fthg = int(data[5 - index])
            ftag = int(data[6 - index])
            ftr = data[7 - index]
            hthg = int(data[8 - index])
            htag = int(data[9 - index])
            b365h = float(data[24 - index])
            b365d = float(data[25 - index])
            b365a = float(data[26 - index])

            fixtures.append(Fixture(div, date, time, home, away, fthg, ftag, ftr, hthg, htag, b365h, b365d, b365a))

        return Table(list(teams.values()), fixtures)

@total_ordering
class Team:
    def __init__(self, name, div):
        self.name = name
        self.div = div
        self.won = 0
        self.lost = 0
        self.drawn = 0
        self.gf = 0
        self.ga = 0
        self.fixtures_played = []

    def play(self, fixture):
        if fixture in self.fixtures_played:
            raise RuntimeError(f"Fixture {fixture} has already been played")
        if fixture.home != self and fixture.away != self:
            raise RuntimeError(f"Fixture {fixture} does not involve team {self}")
        
        if fixture.home == self:
            self.gf += fixture.fthg
            self.ga += fixture.ftag
            if fixture.ftr == 'H':
                self.won += 1
            elif fixture.ftr == 'A':
                self.lost += 1
            elif fixture.ftr == 'D':
                self.drawn += 1
            else:
                raise RuntimeError(f"Invalid match result in {fixture}")
        else:
            self.gf += fixture.ftag
            self.ga += fixture.fthg
            if fixture.ftr == 'H':
                self.lost += 1
            elif fixture.ftr == 'A':
                self.won += 1
            elif fixture.ftr == 'D':
                self.drawn += 1
            else:
                raise RuntimeError(f"Invalid match result in {fixture}")
            
        self.fixtures_played.append(fixture)
        
    def played(self):
        return len(self.fixtures_played)

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

    def __hash__(self):
        return hash((self.name))

@total_ordering
class Fixture:
    def __init__(self, div, date, time, home, away, fthg, ftag, ftr, hthg, htag, b365h, b365d, b365a):
        self.div = div

        # Some data records the year in two digits, some in four
        date_parts = date.split("/")
        if len(date_parts[-1]) == 4:
            self.datetime = datetime.strptime(date + " " + time, "%d/%m/%Y %H:%M")
        else:
            self.datetime = datetime.strptime(date + " " + time, "%d/%m/%y %H:%M")

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

    def play(self):
        self.home.play(self)
        self.away.play(self)

    def __repr__(self):
        return (
            f"Match{{div: {self.div}, datetime: {self.datetime}, home: {self.home}, away: {self.away}, fthg: {self.fthg}, "
            f"ftag: {self.ftag}, ftr: {self.ftr}, hthg: {self.hthg}, htag: {self.htag}, b365h: {self.b365h}, b365d: {self.b365d}, "
            f"b36ga: {self.b365a}}}"
        )

    def __lt__(self, other):
        if other == None or not isinstance(other, Fixture):
            return False

    def __eq__(self, other):
        if other == None or not isinstance(other, Fixture):
            return False

        return self.div == other.div and self.datetime == other.datetime \
                and self.home == other.home and self.away == other.away \
                and self.fthg == other.fthg and self.ftag == other.ftag \
                and self.ftr == other.ftr and self.hthg == other.hthg \
                and self.htag == other.htag and self.b365h == other.b365h \
                and self.b365d == other.b365d and self.b365a == other.b365a
