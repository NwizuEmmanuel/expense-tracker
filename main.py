import csv, argparse,os

filename = "db.csv"

def check_db():
    if not os.path.exists(filename):
        with open(filename, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=["id","description","amount"])
            writer.writeheader()

def main():
    check_db()
    


if __name__ == "__main__":
    main()