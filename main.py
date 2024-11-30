"""Manipulate csv files"""
import csv


def read_file():
    """
    To read csv files
    """
    with open('sample.csv', mode='r', newline='', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)
        print(f"Header: {header}")

        for row in csv_reader:
            print(row)


def add_to_file():
    """Add to csv file"""
    with open('sample.csv', mode='a', newline='', encoding='utf-8') as f:
        data = ['6', 'Spinach', '34.3']
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)


def delete_from_file(index):
    """Delete from csv files"""
    with open('sample.csv', newline='', mode='r', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)
        header = next(csv_reader)
        rows = [row for row in csv_reader if int(row[0]) != index]

    with open('sample.csv', mode='w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)
    print(f"item {index} is delete.")


if __name__ == "__main__":
    read_file()
    delete_from_file(3)
    read_file()
