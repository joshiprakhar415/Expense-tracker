import os
import csv
from datetime import datetime

file="expense.csv"

class Expense:
    # Initializing CSV file
    def initialize_file():
        if not os.path.exists(file):
            with open(file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "date", "description", "amount"])
        else:
            # Check if header is correct
            with open(file, mode='r') as f:
                first_line = f.readline().strip()

            if first_line != "id,date,description,amount":
                print("⚠️ Fixing CSV file (adding header)...")

                with open(file, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "date", "description", "amount"])

    # get id for new expense
    def get_next_id():
        Expense.initialize_file()   # ensure file is correct

        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            ids = []

            for row in reader:
                try:
                    ids.append(int(row["id"]))
                except:
                    continue

            return max(ids, default=0) + 1
        
    # Adding new expense
    def add_expense():
        date = datetime.today().strftime("%Y-%m-%d")
        desc = input("Enter description: ")
        amount = float(input("Enter amount: "))

        exp_id = Expense.get_next_id()

        with open(file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([exp_id, date, desc, amount])

        print("Expense added successfully!")
    
    # Updating existing expense
    def update_expense():
        exp_id = input("Enter ID to update: ")
        rows = []
        found = False

        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == exp_id:
                    print("Leave blank to keep old value")

                    new_date = datetime.today().strftime("%Y-%m-%d")
                    new_desc = input(f"New description ({row['description']}): ") or row['description']
                    new_amount = input(f"New amount ({row['amount']}): ") or row['amount']

                    row = {
                        "id": exp_id,
                        "date": new_date,
                        "description": new_desc,
                        "amount": new_amount
                    }
                    found = True

                rows.append(row)

        if not found:
            print("ID not found")
            return

        with open(file, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "description", "amount"])
            writer.writeheader()
            writer.writerows(rows)

        print("Expense updated!")
    
    # Deleting existing expense
    def delete_expense():
        exp_id = input("Enter ID to delete: ")
        rows = []

        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] != exp_id:
                    rows.append(row)

        with open(file, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "description", "amount"])
            writer.writeheader()
            writer.writerows(rows)

        print("Expense deleted!")
    
    # View all expenses
    def view_expenses():
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            print("\nID | Date | Description | Amount")
            print("-" * 40)
            for row in reader:
                print(f"{row['id']} | {row['date']} | {row['description']} | {row['amount']}")
    
    # View summary of expenses
    def view_summary():
        total = 0

        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += float(row["amount"])

        print(f"\n Total Expenses: ₹{total}")
    
    # View monthly summary
    def view_monthly_summary():
        monthly = {}

        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                month = row["date"][:7]  # YYYY-MM
                amount = float(row["amount"])

                if month in monthly:
                    monthly[month] += amount
                else:
                    monthly[month] = amount

        print("\n Monthly Summary:")
        for month, total in monthly.items():
            print(f"{month}: ₹{total}")
    
    # Main function
    def main():
        Expense.initialize_file()
        while True:
            print("\n--- EXPENSE TRACKER ---")
            print("1. Add Expense")
            print("2. Update Expense")
            print("3. Delete Expense")
            print("4. View Expenses")
            print("5. View Summary")
            print("6. View Monthly Summary")
            print("7. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                Expense.add_expense()

            elif choice == "2":
                Expense.update_expense()

            elif choice == "3":
                Expense.delete_expense()

            elif choice == "4":
                Expense.view_expenses()

            elif choice == "5":
                Expense.view_summary()

            elif choice == "6":
                Expense.view_monthly_summary()

            elif choice == "7":
                break

            else:
                print("Invalid choice")
                continue


Expense.main()