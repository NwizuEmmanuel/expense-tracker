"""Expense tracker"""
import csv
import argparse
import os

FILENAME = "db.csv"


def check_db():
    """
    check for csv file.
    if not in existance will create one and prepare it.
    """
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['id', 'description', 'amount'])


def write_to_db(data, mode):
    """save data to csv"""
    with open(FILENAME, mode, newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)


def read_db():
    """read and get db data"""
    result = {
        "header": [],
        "data": [],
    }
    with open(FILENAME, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        result["header"] = next(csv_reader)
        for item in csv_reader:
            result['data'].append(item)
    return result


def get_id():
    """
    Get the total number of expense and add one to it.
    prepare it for the new expense item.
    """
    index = len(read_db()["data"]) + 1
    return index


def add_expense(args):
    """Expense function"""
    data = [
        get_id(),
        args.description,
        args.amount
    ]
    write_to_db(data=data, mode='a')
    print("saved")
    print(f"{data[0]}. {data[1]}={data[2]}")


def list_expense(_):
    """List expense"""
    for item in read_db()['data']:
        print(f"{item[0]}. {item[1]}: {item[2]}")


def delete_expense(args):
    pass
def main():
    """main func"""
    check_db()
    parser = argparse.ArgumentParser(description="Expense Tracker.")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help="To add new expense.")
    add_parser.add_argument("-d", "--description",
                            required=True, help="Description of expense.")
    add_parser.add_argument("-a", "--amount", type=float,
                            required=True, help="Amount of expense.")
    subparsers.add_parser("list", help="List expenses")

    args = parser.parse_args()
    commands = {
        "add": add_expense,
        "list": list_expense,
    }
    for key, value in commands.items():
        if args.command == key:
            value(args)


if __name__ == "__main__":
    main()
