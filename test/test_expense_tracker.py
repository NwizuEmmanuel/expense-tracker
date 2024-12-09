"""Unit test for expense tracker"""
import unittest
import os
import csv
from app.expense_tracker import DatabaseHandler, ExpenseTracker


class TestExpenseTracker(unittest.TestCase):
    """Unit test class for expense tracker."""

    def setUp(self):
        self.temp_db = "test_db.csv"
        self.db = DatabaseHandler(filename=self.temp_db)
        self.expense_tracker = ExpenseTracker()

    def tearDown(self):
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)

    def test_database_initialization(self):
        """To check column names in database."""
        self.assertTrue(os.path.exists(self.temp_db),
                        "Database file was not created.")
        with open(self.temp_db, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertTrue(header, DatabaseHandler().header)

    
    def test_add_expense(self):
        """Test for add a new expense"""
        self.expense_tracker.args = type('',(),{})()
        self.expense_tracker.args.d = 'Lunch'
        self.expense_tracker.args.a = 15.50
        
        self.expense_tracker.command_add(self.expense_tracker.args)
        
        data = self.db.read_data()['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][1], 'Lunch')
        self.assertEqual(float(data[0][2]), 15.50)

if __name__ == "__main__":
    unittest.main()
