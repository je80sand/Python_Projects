# exptrack.py
# Expense Tracker by Jose Sandoval - with Dates & Monthly Totals

import json
import os
from datetime import datetime, date
from collections import defaultdict

DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Entertainment",
    "Other"
]

expenses = []

def load_expenses():
    """Load expenses from the JSON file if it exists. Backfill date if missing."""
    global expenses
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                expenses = json.load(file)
            except json.JSONDecodeError:
                # If file is empty or invalid, reset to empty list
                expenses = []
    else:
        expenses = []

    # Backfill missing 'date' fields (for older entries) with today's date
    today_iso = date.today().isoformat()
    for e in expenses:
        if "date" not in e:
            e["date"] = today_iso

def save_expenses():
    """Save all expenses to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=2)

def choose_category(prompt="Choose a category"):
    print("\nCategories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {cat}")
    while True:
        choice = input(f"{prompt} (1-{len(CATEGORIES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("⚠️  Invalid choice. Try again.")

def parse_date_input():
    """
    Ask for a date in YYYY-MM-DD. Enter = today.
    Returns ISO date string.
    """
    txt = input("Date (YYYY-MM-DD) — press Enter for today: ").strip()
    if txt == "":
        return date.today().isoformat()
    try:
        d = datetime.strptime(txt, "%Y-%m-%d").date()
        return d.isoformat()
    except ValueError:
        print("⚠️  Invalid date format. Using today instead.")
        return date.today().isoformat()

def add_expense():
    name = input("\nExpense name: ").strip()
    while not name:
        print("⚠️  Name cannot be empty.")
        name = input("Expense name: ").strip()

    while True:
        amt_txt = input("Amount (numbers only): ").strip()
        try:
            amount = float(amt_txt)
            if amount < 0:
                raise ValueError
            break
        except ValueError:
            print("⚠️  Please enter a valid non-negative number.")

    category = choose_category("Choose a category")
    when = parse_date_input()

    expenses.append({
        "name": name,
        "amount": amount,
        "category": category,
        "date": when
    })
    save_expenses()
    print(f"✅ Added: {name} — ${amount:.2f} [{category}] on {when}")

def view_expenses(filtered=None, title="All Expenses"):
    """
    Show a list of expenses.
    filtered: optional list of expense dicts to display.
    """
    items = filtered if filtered is not None else expenses
    print("\n#  Date        Name                          Amount    Category")
    print("-- ----------  ---------------------------- --------- -----------")
    total = 0.0
    for idx, e in enumerate(items, start=1):
        total += float(e["amount"])
        print(f"{idx:>2} {e['date']}  {e['name'][:28]:<28} ${float(e['amount']):>7.2f}  {e['category']}")
    print("---------------------------------------------------------------")
    print(f"   Total ------------------------------->   ${total:>7.2f}\n")

def delete_expense():
    view_expenses(title="All Expenses")
    if not expenses:
        return
    try:
        choice = int(input("Enter expense number to delete: ").strip())
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            save_expenses()
            print(f"🗑️  Deleted: {removed['name']} (${removed['amount']:.2f})")
        else:
            print("⚠️  Invalid number.")
    except ValueError:
        print("⚠️  Please enter a valid number.")

def view_by_category():
    cat = choose_category("View which category")
    filtered = [e for e in expenses if e["category"] == cat]
    if not filtered:
        print(f"\n(No expenses in '{cat}')\n")
        return
    print(f"\n== {cat} ==")
    view_expenses(filtered=filtered, title=f"{cat} Expenses")

def totals_by_category():
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += float(e["amount"])
    print("\nCategory Totals:")
    for cat in CATEGORIES:
        print(f"  {cat:<12} ${totals[cat]:>7.2f}")
    print()

def totals_by_month():
    """
    Group totals by YYYY-MM (e.g., 2025-10).
    """
    monthly = defaultdict(float)
    for e in expenses:
        # e['date'] is ISO (YYYY-MM-DD). Take first 7 chars for YYYY-MM
        ym = e["date"][:7] if "date" in e and len(e["date"]) >= 7 else date.today().strftime("%Y-%m")
        monthly[ym] += float(e["amount"])

    print("\nMonthly Totals:")
    for ym in sorted(monthly.keys()):
        print(f"  {ym}: ${monthly[ym]:>7.2f}")
    print()

def show_menu():
    print("\n==== Expense Tracker ====")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Delete Expense")
    print("4. View by Category")
    print("5. Totals by Category")
    print("6. Totals by Month  ✅ NEW")
    print("7. Exit")

# Main Program
load_expenses()
while True:
    show_menu()
    choice = input("Choose an option (1–7): ").strip()
    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        delete_expense()
    elif choice == "4":
        view_by_category()
    elif choice == "5":
        totals_by_category()
    elif choice == "6":
        totals_by_month()
    elif choice == "7":
        print("👋 Goodbye, Jose! Keep budgeting smart!")
        break
    else:
        print("⚠️  Invalid choice. Please select 1–7.")
