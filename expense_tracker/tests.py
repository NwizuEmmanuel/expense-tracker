import unittest
import csv
from main import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    TEST_DB = "test_db.csv"
    
    def setUp(self):
        ExpenseTracker.FILENAME = self.TEST_DB
        with open(self.TEST_DB, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(ExpenseTracker.HEADERS)
        return super().setUp()