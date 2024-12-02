"""Expense tracker"""

from datetime import datetime
import csv
import argparse
import os
import calendar
import sys


class ExpenseTracker():
    """Expense Tracker Main class"""
    FILENAME = "db.csv"
    HEADERS = ['id', 'description', 'amount', 'date']

    parser = None
    subparsers = None
    args = None

    def __init__(self):
        self.check_db()
        self.parser = argparse.ArgumentParser(description="Expense Tracker.")
        self.subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands")
        self.add_commands()
        self.args = self.parser.parse_args()


    def run_command(self):
        """To run commands"""
        commands = {
            "add": self.add_expense,
            "list": self.list_expense,
            "delete": self.delete_expense,
            'summary': self.summary
        }
        for key, value in commands.items():
            if self.args.command == key:
                value()

    def check_db(self):
        """
        check for csv file.
        if not in existance will create one and prepare it.
        """
        if not os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'a', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(self.HEADERS)

    def write_to_db(self, data, mode, header=None):
        """save data to csv"""
        with open(self.FILENAME, mode, newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            if mode == 'w':
                csv_writer.writerow(header)
                csv_writer.writerows(data)
            else:
                csv_writer.writerow(data)

    def read_db(self):
        """read and get db data"""
        result = {
            "header": [],
            "data": [],
        }
        with open(self.FILENAME, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            result["header"] = next(csv_reader)
            for item in csv_reader:
                result['data'].append(item)
        return result

    def get_id(self):
        """
        Get the total number of expense and add one to it.
        prepare it for the new expense item.
        """
        index = len(self.read_db()["data"]) + 1
        return index

    def add_expense(self):
        """Expense function"""
        now = datetime.now()
        data = [
            self.get_id(),
            self.args.description,
            self.args.amount,
            now.strftime('%Y-%m-%d %H:%M:%S')
        ]
        self.write_to_db(data=data, mode='a')
        print("saved")
        print(f"{data[0]}. {data[1]}={data[2]} ({data[3]})")

    def list_expense(self):
        """List expense"""
        for item in self.read_db()['data']:
            print(f"{item[0]}. {item[1]}: {item[2]} ({item[3]})")

    def delete_expense(self):
        """delete expense"""
        new_data = [item for item in self.read_db()['data']
                    if int(item[0]) != self.args.id]
        self.write_to_db(data=new_data, mode='w', header=self.HEADERS)
        print(f"Expense delete: {self.args.id}")

    def get_month_name(self, month_number):
        """get month index"""
        if 1 <= month_number <= 12:
            return calendar.month_name[month_number]
        return month_number

    def summary(self):
        """To get the summary"""
        data = self.read_db()["data"]
        result = 0
        if not self.args.month > 0:
            for item in data:
                result += float(item[2])
            print(f"Total expense: {result}")
        else:
            for item in data:
                datetime_obj = datetime.strptime(
                    item[3], '%Y-%m-%d %H:%M:%S')
                result += float(item[2]
                                ) if datetime_obj.month == self.args.month else 0
            print(f"Total expense for {
                  self.get_month_name(self.args.month)}: {result}")

    def add_commands(self):
        """To add these commands when this class is initialized."""
        add_parser = self.subparsers.add_parser(
            "add", help="To add new expense.")
        add_parser.add_argument("-d", "--description",
                                help="Description of expense.")
        add_parser.add_argument(
            "-a", "--amount", type=float, help="Amount of expense.")

        _ = self.subparsers.add_parser("list", help="List expenses")

        delete_parser = self.subparsers.add_parser(
            "delete", help="To delete expense.")
        delete_parser.add_argument(
            "id", type=int, help="Expense ID to delete.")

        summary_parser = self.subparsers.add_parser(
            "summary", help="To summarize expense")
        summary_parser.add_argument(
            "--month", type=int, help="Filter with month.", default=0)

def main():
    """main function"""
    app = ExpenseTracker()
    app.run_command()


if __name__ == "__main__":
    main()
