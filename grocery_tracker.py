from datetime import date, timedelta
import csv

def load_files():
    current_groceries = []
    reference = {}

    with open('./data/curr.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            current_groceries.append([row['grocery'], row['date_received'], row['good_until']])
    with open('./data/ref.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            reference[row['grocery']] = int(row['shelf_life'])
    return (current_groceries, reference)
    

def save_files(current_groceries, reference):
    print(current_groceries)
    print(reference)
    with open('./data/curr.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['grocery','date_received','good_until'])
        for item in current_groceries:
            writer.writerow(item)
    with open('./data/ref.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['grocery','shelf_life'])
        for key, value in reference.items():
            writer.writerow([key, value])


def add_grocery(current_groceries, reference):
    grocery = input('Grocery: ')
    date_received = date.today()
    if grocery not in reference:
        shelf_life = int(input('Shelf life: '))
        reference[grocery] = shelf_life

    good_until = date_received + timedelta(days=reference[grocery])
    current_groceries.append([grocery, date_received, good_until])

def main():
    # load file
    current_groceries, reference = load_files()

    # prompt action on loop
    loop_flag = True
    while loop_flag:
        add_grocery(current_groceries, reference)
        loop_flag = input('Add grocery? (Y/N): ') != 'N'

    # save file
    save_files(current_groceries, reference)


main()