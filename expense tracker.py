import json
import os
from datetime import datetime
from collections import defaultdict

# File to store expense data
DATA_FILE = "expenses.json"

# Predefined categories
CATEGORIES = ["Food", "Transportation", "Entertainment", "Shopping", "Miscellaneous"]

# Utility functions
def load_expenses():
    """Load expenses from the data file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    """Save expenses to the data file."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# Input validation
def validate_float(input_str):
    """Validate that input is a non-negative float."""
    try:
        value = float(input_str)
        if value < 0:
            raise ValueError
        return value
    except ValueError:
        return None

def validate_date(input_str):
    """Validate the date input."""
    try:
        return datetime.strptime(input_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None

def get_category():
    """Prompt user to select or add a category."""
    print("\nCategories:")
    for idx, category in enumerate(CATEGORIES, 1):
        print(f"{idx}. {category}")
    print(f"{len(CATEGORIES) + 1}. Add a new category")

    while True:
        choice = input("Choose a category (number): ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            elif choice == len(CATEGORIES) + 1:
                new_category = input("Enter new category name: ").strip()
                if new_category:
                    CATEGORIES.append(new_category)
                    return new_category
        print("Invalid choice. Please try again.")

# Core functionalities
def add_expense():
    """Add a new expense."""
    print("\n--- Add Expense ---")
    while True:
        amount = validate_float(input("Enter amount: "))
        if amount is not None:
            break
        print("Invalid amount. Please enter a non-negative number.")
    
    description = input("Enter description: ").strip()
    category = get_category()
    
    while True:
        date = validate_date(input("Enter date (YYYY-MM-DD, press Enter for today): ") or datetime.now().strftime("%Y-%m-%d"))
        if date:
            break
        print("Invalid date format. Please try again.")

    expense = {
        "date": date,
        "amount": amount,
        "description": description,
        "category": category,
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!")

def view_summary():
    """View monthly summary of expenses."""
    print("\n--- Monthly Summary ---")
    year = input("Enter year (YYYY): ")
    month = input("Enter month (MM): ")
    
    expenses = load_expenses()
    filtered = [e for e in expenses if e["date"].startswith(f"{year}-{month:02}")]
    
    if not filtered:
        print("No expenses found for the specified month.")
        return

    total = sum(e["amount"] for e in filtered)
    print(f"\nTotal expenses for {year}-{month}: {total:.2f}\n")
    print("Details:")
    for e in filtered:
        print(f"- {e['date']}: {e['description']} (${e['amount']:.2f}) [{e['category']}]")

def view_category_analysis():
    """View category-wise analysis."""
    print("\n--- Category Analysis ---")
    expenses = load_expenses()

    if not expenses:
        print("No expenses recorded.")
        return

    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e["category"]] += e["amount"]

    print("\nCategory-wise Expenditure:")
    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")

    total_expenses = sum(category_totals.values())
    print(f"\nTotal Expenses: ${total_expenses:.2f}")
    print("Category Breakdown (%):")
    for category, total in category_totals.items():
        percentage = (total / total_expenses) * 100
        print(f"{category}: {percentage:.2f}%")

# User Interface
def main_menu():
    """Display the main menu."""
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Monthly Summary")
        print("3. View Category-Wise Analysis")
        print("4. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            view_category_analysis()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point
if __name__ == "__main__":
    main_menu()
