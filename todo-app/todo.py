"""My Terminal To-Do List App.

Run it with:  python todo.py

The app shows a menu, keeps tasks in a list of dictionaries,
and saves them to tasks.json so they survive restarts.
"""


from storage import load_tasks, save_tasks


# ---------------------------------------------------------------
# Task functions: pure logic. They take `tasks` (a list of
# dictionaries), do one job, and return a result.
# No input() or print() in here, so tests can check them easily.
# ---------------------------------------------------------------


def next_task_id(tasks):
    """Return the next free task ID.

    We use max(existing IDs) + 1 so a deleted task's ID
    is never reused (which would confuse the user).
    First task ever gets ID 1.
    """

    highest_id = 0

    for task in tasks:
        if task["id"] > highest_id:
            highest_id = task["id"]

    return highest_id + 1


def find_task(tasks, task_id):
    """Return the task dictionary with the given ID, or None if not found."""

    for task in tasks:
        if task["id"] == task_id:
            return task

    return None


def add_task(tasks, description):
    """Add a new task and return it.

    Rejects empty descriptions (after removing extra spaces)
    by raising a ValueError, which the menu catches and shows.
    """

    description = description.strip()

    if not description:
        raise ValueError("Task description cannot be empty.")

    task = {
        "id": next_task_id(tasks),
        "description": description,
        "done": False,
    }

    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    """Mark a task as completed. Return True on success, False if not found."""

    task = find_task(tasks, task_id)

    if task is None:
        return False

    task["done"] = True
    return True


def delete_task(tasks, task_id):
    """Remove a task. Return True on success, False if not found."""

    task = find_task(tasks, task_id)

    if task is None:
        return False

    tasks.remove(task)
    return True


# ---------------------------------------------------------------
# Display functions: only READING and PRINTING, no changes.
# ---------------------------------------------------------------


def format_status(task):
    """Return 'completed' or 'pending' for one task."""

    if task["done"]:
        return "completed"

    return "pending"


def display_tasks(tasks):
    """Print all tasks in a readable, numbered-by-ID format."""

    print("\n--- MY TASKS ---")

    if not tasks:
        print("No tasks yet. Add one from the menu!")
        return

    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {format_status(task)}")


def display_menu():
    """Print the main menu."""

    print("\n==== MY TO-DO LIST ====")
    print("1. View tasks")
    print("2. Add a task")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. Exit")


# ---------------------------------------------------------------
# Menu actions: talk to the user, use the task functions above,
# then save to the JSON file after every change.
# ---------------------------------------------------------------


def add_task_menu(tasks):
    """Ask the user for a description and add the task."""

    description = input("Enter the task description: ")

    try:
        task = add_task(tasks, description)

    except ValueError as error:
        print(f"Could not add task: {error}")
        return

    save_tasks(tasks)
    print(f"Task added with ID {task['id']}.")


def complete_task_menu(tasks):
    """Ask for a task ID and mark that task completed."""

    raw_id = input("Enter the ID of the task to complete: ").strip()

    try:
        task_id = int(raw_id)

    except ValueError:
        print("That is not a number. Please enter a task ID like 3.")
        return

    if complete_task(tasks, task_id):
        save_tasks(tasks)
        print(f"Task {task_id} marked as completed.")

    else:
        print(f"No task found with ID {task_id}.")


def delete_task_menu(tasks):
    """Ask for a task ID and delete that task."""

    raw_id = input("Enter the ID of the task to delete: ").strip()

    try:
        task_id = int(raw_id)

    except ValueError:
        print("That is not a number. Please enter a task ID like 3.")
        return

    if delete_task(tasks, task_id):
        save_tasks(tasks)
        print(f"Task {task_id} deleted.")

    else:
        print(f"No task found with ID {task_id}.")


def read_menu_choice():
    """Ask for a menu choice. Keeps asking until it is a valid option."""

    while True:
        choice = input("\nChoose an option (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")


def main():
    """Run the application: load saved tasks, then show the menu loop."""

    tasks = load_tasks()

    print("Welcome to My To-Do List!")

    while True:
        display_menu()
        choice = read_menu_choice()

        if choice == "1":
            display_tasks(tasks)

        elif choice == "2":
            add_task_menu(tasks)

        elif choice == "3":
            complete_task_menu(tasks)

        elif choice == "4":
            delete_task_menu(tasks)

        elif choice == "5":
            print("Goodbye! Your tasks are saved.")
            break


if __name__ == "__main__":
    main()
