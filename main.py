import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


def initialize_file():
    """Create the expense file if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Note"])


def add_expense():
    print("\n--- ADD EXPENSE ---")

    category = input("Category (Food/Travel/College/Shopping/Other): ").strip()

    while True:
        try:
            amount = float(input("Amount (₹): "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid amount.")

    note = input("Note: ").strip()
    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, note])

    print("✓ Expense added successfully!")


def view_expenses():
    print("\n--- ALL EXPENSES ---")

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        expenses = list(reader)

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("-" * 65)
    print(f"{'Date':<12}{'Category':<15}{'Amount':<12}{'Note'}")
    print("-" * 65)

    for expense in expenses:
        print(
            f"{expense['Date']:<12}"
            f"{expense['Category']:<15}"
            f"₹{float(expense['Amount']):<11.2f}"
            f"{expense['Note']}"
        )

    print("-" * 65)


def show_summary():
    print("\n--- SPENDING SUMMARY ---")

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        expenses = list(reader)

    if not expenses:
        print("No expenses recorded yet.")
        return

    total = 0
    categories = {}

    for expense in expenses:
        amount = float(expense["Amount"])
        category = expense["Category"]

        total += amount
        categories[category] = categories.get(category, 0) + amount

    print(f"\nTotal spent: ₹{total:.2f}")

    print("\nCategory-wise spending:")
    for category, amount in sorted(
        categories.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"  {category:<15} ₹{amount:.2f}")

    highest_category = max(categories, key=categories.get)

    print(
        f"\nHighest spending category: "
        f"{highest_category} (₹{categories[highest_category]:.2f})"
    )


def search_expenses():
    keyword = input("\nEnter category or keyword to search: ").strip().lower()

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        results = []

        for expense in reader:
            if (
                keyword in expense["Category"].lower()
                or keyword in expense["Note"].lower()
            ):
                results.append(expense)

    if not results:
        print("No matching expenses found.")
        return

    print("\n--- SEARCH RESULTS ---")

    for expense in results:
        print(
            f"{expense['Date']} | "
            f"{expense['Category']} | "
            f"₹{float(expense['Amount']):.2f} | "
            f"{expense['Note']}"
        )


def main():
    initialize_file()

    while True:
        print("\n")
        print("=" * 40)
        print("          SPENDWISE")
        print("      Personal Expense Tracker")
        print("=" * 40)

        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Spending Summary")
        print("4. Search Expenses")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            show_summary()

        elif choice == "4":
            search_expenses()

        elif choice == "5":
            print("\nThank you for using SpendWise!")
            break

        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
