# tracker.py
# Personal Productivity Tracker by Jose Sandoval
import json
import os

DATA_FILE = "task.json"
tasks = []

def load_tasks():
    """Load tasks from the JSON file if it exists."""
    global tasks
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

def save_tasks():
    """Save all tasks to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def show_menu():
    print("\n==== Productivity Tracker ====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Complete")
    print("4. Exit")

def add_task():
    task_name = input("Enter task name: ")
    tasks.append({"name": task_name, "completed": False})
    save_tasks()
    print(f"✅ Task '{task_name}' added!")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, 1):
            status = "✅ Done" if task["completed"] else "⏳ In Progress"
            print(f"{i}. {task['name']} - {status}")

def mark_complete():
    view_tasks()
    try:
        num = int(input("\nEnter task number to mark complete: "))
        tasks[num - 1]["completed"] = True
        save_tasks()
        print(f"🎉 Task '{tasks[num - 1]['name']}' marked complete!")
    except (ValueError, IndexError):
        print("⚠️ Invalid task number.")

# === Main Program ===
load_tasks()

while True:
    show_menu()
    choice = input("Choose an option (1-4): ")
    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_complete()
    elif choice == "4":
        save_tasks()
        print("👋 Goodbye, Jose! Stay productive!")
        break
    else:
        print("⚠️ Invalid choice. Please select 1-4.")
