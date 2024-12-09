"""Main module"""
from app.expense_tracker import ExpenseTracker

def main(args=None):
    """Main function"""
    app = ExpenseTracker()
    app.run(args)


if __name__ == "__main__":
    main()
