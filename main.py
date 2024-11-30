"""Expense tracker"""

from datetime import datetime
import csv
import argparse
import os

FILENAME = "db.csv"
HEADERS = ['id', 'description', 'amount','date']


def check_db():
    """
    check for csv file.
    if not in existance will create one and prepare it.
    """
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(HEADERS)


def write_to_db(data, mode, header=None):
    """save data to csv"""
    with open(FILENAME, mode, newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        if mode == 'w':
            csv_writer.writerow(header)
            csv_writer.writerows(data)
        else:
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
    now = datetime.now()
    now = now.strftime("%d/%m/%Y")
    data = [
        get_id(),
        args.description,
        args.amount,
        now
    ]
    write_to_db(data=data, mode='a')
    print("saved")
    print(f"{data[0]}. {data[1]}={data[2]} ({data[3]})")


def list_expense(_):
    """List expense"""
    for item in read_db()['data']:
        print(f"{item[0]}. {item[1]}: {item[2]}")


def delete_expense(args):
    """delete expense"""
    new_data = [item for item in read_db()['data'] if int(item[0]) != args.id]
    write_to_db(data=new_data, mode='w', header=HEADERS)
    print(f"Expense delete: {args.id}")


def summary(args):
    """To get the summary"""
    data = read_db()["data"]
    result = 0
    for item in data:
        result += float(item[2])

    if args.month > 0:
        pass
    print(f"Total: {result}")


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

    _ = subparsers.add_parser("list", help="List expenses")

    delete_parser = subparsers.add_parser("delete", help="To delete expense.")
    delete_parser.add_argument("id", type=int, help="Expense ID to delete.")

    summary_parser = subparsers.add_parser("summary", help="To summarize expense")
    summary_parser.add_argument("--month", type=int, help="Filter with month.")

    args = parser.parse_args()
    commands = {
        "add": add_expense,
        "list": list_expense,
        "delete": delete_expense,
        'summary': summary
    }
    for key, value in commands.items():
        if args.command == key:
            value(args)


if __name__ == "__main__":
    main()
