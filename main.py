from models import Table, Team, Match

def run():
    with open('data/E0.csv', 'r') as file:
        table = Table.load_data_from_file(file)

    

if __name__ == "__main__": 
    run()