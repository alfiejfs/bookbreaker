from models import Table, Team, Fixture
from matchrunner import MatchRunner
from strategies.alwayshome import AlwaysHome
from strategies.alwaysaway import AlwaysAway
from strategies.alwaysdraw import AlwaysDraw

def run():
    season = input("Which season do you want to use: ")
    with open(f'data/prem-{season}.csv', 'r') as file:
        table = Table.load_data_from_file(file)

    match_runner = MatchRunner(table)
    
    strategy = AlwaysAway(match_runner.table, 10)

    profit = 0
    loss = 0

    while match_runner.can_run():
        fixture = match_runner.table.get_next_fixture()
        bet = strategy.handle_fixture(fixture)

        if bet.check():
            profit += bet.get_profit()
        else:
            loss += bet.get_loss()

        match_runner.run()

    overall = profit - loss
    marker = "+" if overall > 0 else ""

    print (f"Betting away only P/L = +{profit:.2f}/-{loss:.2f}")
    print(f"Overall profit or loss for season: {marker}{overall:.2f}")


if __name__ == "__main__": 
    run()