import pytest
import os
from app.expense_tracker import DatabaseHandler, ExpenseTracker
from datetime import datetime
import logging


class TestExpenseTracker():
    """Beginning of test class"""

    def setUp(self):
        self.filename = 'temp_db.csv'
        self.db = DatabaseHandler(filename=self.filename)
        self.tracker = ExpenseTracker()
        self.db.check_db()

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
