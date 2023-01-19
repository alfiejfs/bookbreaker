from matchmodels import Table
from matchrunner import MatchRunner

from strategies.topsix import TopSix
from strategies.alwayshigherpoints import AlwaysHigherPoints
from strategies.alwaysaway import AlwaysAway
from strategies.poundperpoint import PoundPerPoint
from strategies.poundperpointtopsix import PoundPerPointTopSix

def run_all_seasons(strategy_class):
    total_overall = 0
    total_staking = 0
    for i in range(12, 22):
        with open(f'data/prem-{i}-{i + 1}.csv', 'r') as file:
            table = Table.load_data_from_file(file)

        match_runner = MatchRunner(table)

        strategy = strategy_class(table, 10)

        profit = 0  
        loss = 0

        while match_runner.can_run():
            fixture = match_runner.table.get_next_fixture()
            bet = strategy.calculate_fixture(fixture)

            if bet is not None:
                if bet.won():
                    profit += bet.get_return()
                else:
                    loss += bet.get_return()

            match_runner.run()

        overall = profit + loss
        marker = "+" if overall > 0 else ""

        print(f"Season {i}-{i + 1}")
        print(f"Total staked: {strategy.total_stake}")
        print(f"Betting away only P/L = +{profit:.2f}/-{loss:.2f}")
        print(f"Overall profit or loss for season: {marker}{overall:.2f}")
        print(f"Overall/Stake for season: {overall/strategy.total_stake}")
        print("")
        total_overall += overall
        total_staking += strategy.total_stake

    marker = "+" if total_overall > 0 else ""
    print(f"Total staked: {total_staking}")
    print(f"Total overall: {marker}{total_overall:.2f}")
    print(f"Overall/Stake: {total_overall/total_staking}")
    

if __name__ == "__main__":
    #print("Top Six (>= 10 games played for both teams")
    #run_all_seasons(TopSix)

    print("\n\n**\n\nAlways Away")
    run_all_seasons(AlwaysAway)

    #print("\n\n**\n\nAlways Higher Points")
    #run_all_seasons(AlwaysHigherPoints)

    #print("\n\n**\n\nPound Per Point")
    #run_all_seasons(PoundPerPoint)

    print("\n\n**\n\nPound Per Point Top Six (>= 5 games played")
    run_all_seasons(PoundPerPointTopSix)