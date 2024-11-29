import csv, argparse,os

filename = "db.csv"

def check_db():
    if not os.path.exists(filename):
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id","description","amount"])
            writer.writeheader()

def save_to_db(data: dict):
    fieldnames = list(data.keys())
    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

def give_index():
    index = 1
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            index += 1
    return index
    
def add_expense(args=None):
    data = {
        'id': give_index(),
        'description': args.description,
        'amount': args.amount
    }
    save_to_db(data=data)
    print("saved")
    print(f"{data['id']}. {data['description']}={data['amount']}")


def list_expense(args=None):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"{row['id']}. {row['description']} => {row['amount']}")

def main():
    check_db()
    parser = argparse.ArgumentParser(description="Expense Tracker.")
    subparsers = parser.add_subparsers(dest='command', help="Available commands")

    add_parser = subparsers.add_parser("add", help="Add new expense.")
    add_parser.add_argument("-d", "--description", required=True, help="Description of expense.")
    add_parser.add_argument("-a","--amount", type=int, required=True, help="Amount of expense.")

    subparsers.add_parser("list", help="List expenses.") # for listing expenses.

    delete_parser = subparsers.add_parser("delete", help="Delete an expense item")
    delete_parser.add_argument("id", type=int, help="Expense item id")

    args = parser.parse_args()
    commands = {
        "add":add_expense,
        'list': list_expense,
    }
    for c in commands:
        if args.command == c:
            commands[c](args)

if __name__ == "__main__":
    main()