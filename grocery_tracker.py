from datetime import date, datetime, timedelta
import csv

class GroceryTracker:
    def __init__(self, curr, ref):
        self.curr_path = curr
        self.ref_path = ref
        self.current_groceries = []
        self.reference = {}
        self.load_files()

    def load_files(self):
        with open(self.curr_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.current_groceries.append([row['grocery'], datetime.strptime(row['date_received'], '%Y-%m-%d').date(), datetime.strptime(row['good_until'], '%Y-%m-%d').date()])
        with open(self.ref_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.reference[row['grocery']] = int(row['shelf_life'])


    def save_files(self):
        with open(self.curr_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['grocery','date_received','good_until'])
            for item in self.current_groceries:
                writer.writerow(item)
        with open(self.ref_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['grocery','shelf_life'])
            for key, value in self.reference.items():
                writer.writerow([key, value])


    def show_groceries(self):
        if input('show current groceries? (y to show): ') == 'y':
            print('grocery\t\tdate_received\t\tgood_until\t\tdays_left')
            for item in self.current_groceries:
                days_left = (item[2] - date.today()).days
                print('{}\t\t{}\t\t{}\t\t{}'.format(item[0], item[1], item[2], days_left))


    def add_groceries(self):
        loop_flag = input('add grocery? (n to exit): ') != 'n'
        while loop_flag:
            grocery = input('grocery: ')
            date_received = input('date (YYYY-MM-DD): ') 
            date_received = date.today() if date_received == '' else datetime.strptime(date_received, '%Y-%m-%d').date()

            if grocery not in self.reference:
                shelf_life = int(input('shelf life: '))
                self.reference[grocery] = shelf_life
            good_until = date_received + timedelta(days=self.reference[grocery])
            self.current_groceries.append([grocery, date_received, good_until])

            loop_flag = input('add grocery? (n to exit): ') != 'n'
    
    
def main():
    # load file
    tracker = GroceryTracker('./data/curr.csv', './data/ref.csv')
    # prompt action on loop
    tracker.show_groceries()
    tracker.add_groceries()
    tracker.show_groceries()

    # save file
    tracker.save_files()

main()