import argparse
import csv
import os

filename = "expenses.csv" # csv file name
fieldnames = ['id','description','amount'] # columns header for csv header

# check if csv header exists
def check_file():
    if not os.path.exists(filename):
        with open(filename, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

# to save to csv file
def save_to_file(data):
    with open(filename, 'a')as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

# for adding index (id) for new expense item
def get_id():
    index = 0
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            index += 1
    index += 1
    return index

# func for adding new expense item  
def add_expense(args):
    data = {
        'id':get_id(),
        'description': args.description,
        'amount': args.amount
    }
    with open(filename, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(data)

def add_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="command", help="Available commands.")

    # add command
    add_parser = subparsers.add_parser("add", help="To add a new expense item.")
    add_parser.add_argument("-d","--description", type=str, help="Description of expense item", required=True)
    add_parser.add_argument("-a", "--amount", type=int, help="Amount of expense item", required=True)

commands = {
    'add': add_expense
}
def main():
    check_file()

    parser = argparse.ArgumentParser()
    add_parser(parser)
    
    args = parser.parse_args()
    for item in commands:
        if args.command == item:
            commands[item](args)

if __name__ == "__main__":
    main()