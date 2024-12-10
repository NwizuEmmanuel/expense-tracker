"""Expense tracker"""

from datetime import datetime
import csv
import argparse
import os
import calendar
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class DatabaseHandler:
    """Handles database operation for the expense tracker."""

    def __init__(self, filename="db.csv"):
        self.filename = filename
        self.header = ['id', 'description', 'amount', 'date']
        self.check_db()

    def check_db(self):
        """Check if the database exists, and create it if not."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w',
                      newline='',
                      encoding='utf-8') as file:
                csv.writer(file).writerow(self.header)

    def read_data(self):
        """Read and return all data from database"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        return {'header': data[0], 'data': data[1:]}

    def write_data(self, data, mode='w'):
        """write data to database"""
        with open(self.filename, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if mode == 'w':
                writer.writerow(self.header)
            writer.writerows(data)


class ExpenseTracker:
    """Expense Tracker application"""

    def __init__(self):
        self.db = DatabaseHandler()
        self.parser = argparse.ArgumentParser(
            description="Expense Tracker CLI")
        self.subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands")
        self.add_commands()

    def run(self):
        """Parse arguments and execute the corresponding command"""
        args = self.parser.parse_args()
        if args.command:
            try:
                command_func = getattr(self, f"command_{args.command}")
                command_func(args)
            except AttributeError:
                logging.error("Command not implemented.")
        else:
            self.parser.print_help()

    def add_commands(self):
        """Define CLI commands."""
        add_parser = self.subparsers.add_parser("add", help="Add new expense.")
        add_parser.add_argument(
            "-d", "--description", required=True,
            help="Description of the expense.")
        add_parser.add_argument(
            "-a", "--amount",
            type=float, required=True,
            help="Amount of the expense.")

        self.subparsers.add_parser("list", help="List all expenses.")

        delete_parser = self.subparsers.add_parser(
            "delete", help="Delete an expense by ID.")
        delete_parser.add_argument(
            "id", type=int, help="ID of the expense to delete.")

        summary_parser = self.subparsers.add_parser(
            "summary", help="Summarize expenses.")
        summary_parser.add_argument(
            "--month", '-m', type=int,
            help="Summarize for a specific month (1-12)",
            default=0)

    def generate_id(self):
        """
        Generate a new unique ID for the expense.
        """
        data = self.db.read_data()['data']
        return len(data) + 1 if data else 1

    def command_add(self, args):
        """Add a new expense."""
        now = datetime.now()
        data = [
            self.generate_id(),
            args.description,
            args.amount,
            now.strftime('%Y-%m-%d %H:%M:%S')
        ]
        self.db.write_data([data], mode='a')
        logging.info("Expense added: %s - %s on %s", data[1], data[2], data[3])

    def command_list(self, _):
        """List all expenses."""
        data = self.db.read_data()['data']
        if not data:
            logging.info("No expenses found.")
            return

        for item in data:
            print(f"{item[0]}. {item[1]}: {item[2]} ({item[3]})")

    def command_delete(self, args):
        """Delete an expense by ID."""
        data = self.db.read_data()['data']
        new_data = [item for item in data if int(item[0]) != args.id]

        if len(new_data) == len(data):
            logging.warning("No expense found with ID: %s", args.id)
        else:
            self.db.write_data(data=new_data, mode='w')
            logging.info("Expense deleted with ID: %s", args.id)

    def command_summary(self, args):
        """Summarize expenses."""
        data = self.db.read_data()['data']
        if not data:
            logging.info("No expenses to summarize.")
            return

        total = 0
        month = args.month
        for item in data:
            date = datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S')
            if month in {0, date.month}:
                total += float(item[2])

        if month > 0:
            logging.info("Total expenses for %s: %s",
                         calendar.month_name[month], total)
        else:
            logging.info("Total expense: %s", total)
