import csv, argparse,os

filename = "db.csv"

def check_db():
    if not os.path.exists(filename):
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id","description","amount"])
            writer.writeheader()

def save_to_db(data):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file)
        writer.writerow()

def add_expense(args):
    data = {
        'id': args.id,
        'description': args.description,
        'amount': args.amount
    }
    save_to_db(data=data)
    print("saved")
    print(f"{data['id']}. {data['description']}={data['amount']}")


def main():
    check_db()
    parser = argparse.ArgumentParser(description="Expense Tracker.")
    subparsers = parser.add_subparsers(help="Available commands")

    add_parser = subparsers.add_parser("add", help="To add new expense.")
    add_parser.add_argument("-d", "--description", required=True, help="Description of expense.")
    add_parser.add_argument("-a","--amount", type=int, required=True, help="Amount of expense.")

    args = parser.parse_args()
    commands = {
        "add":add_expense
    }
    for c in commands:
        if args.command == c:
            commands[c]()

if __name__ == "__main__":
    main()