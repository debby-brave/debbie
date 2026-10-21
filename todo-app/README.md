# My Terminal To-Do List App

A beginner-friendly to-do list application that runs entirely in the
terminal (command line). Written in Python using only the standard
library — no frameworks, no databases, no web technologies.

## Project description

This app lets you keep a personal task list from your terminal. You can
add tasks, view them with unique IDs and status, mark them completed,
and delete them. Tasks are saved to a JSON file, so closing and
reopening the app never loses your work.

## Features

1. **Add a task** — enter a description; empty descriptions are rejected.
2. **View all tasks** — shows ID, description, and `pending`/`completed` status.
3. **Mark a task completed** — select by ID; invalid IDs are handled gracefully.
4. **Delete a task** — remove by ID; missing IDs are handled gracefully.
5. **Persistence** — tasks are saved to `tasks.json` after every change and
   loaded when the app starts.
6. **Safe exit** — menu option 5 exits cleanly.
7. **Edge cases handled** — empty task lists, invalid menu choices,
   invalid task IDs, missing/empty/corrupt data files.

## Requirements

- Python 3.6 or newer (only the standard library is used — nothing to install)

## How to run the application

```
cd todo-app
python todo.py
```

(On some computers the command is `python3 todo.py`.)

## How to use each menu option

| Option | What it does | Example |
|---|---|---|
| 1. View tasks | Prints every task with its ID and status | `[2] buy milk - pending` |
| 2. Add a task | Prompts for a description, saves immediately | type `buy milk` → `Task added with ID 2.` |
| 3. Mark completed | Prompts for a task ID, sets it to completed | type `2` → `Task 2 marked as completed.` |
| 4. Delete a task | Prompts for a task ID, removes it | type `2` → `Task 2 deleted.` |
| 5. Exit | Saves nothing extra (changes are already saved) | `Goodbye! Your tasks are saved.` |

Typing anything other than 1–5 at the menu re-prompts; it never crashes.

## Explanation of the files

| File | Purpose |
|---|---|
| `todo.py` | The application: task functions, menu, and the main loop |
| `storage.py` | One job only: saving/loading the JSON file |
| `tests/test_todo.py` | Automated tests (never touches your real data) |
| `tasks.json` | Your saved tasks (created automatically on first save; not committed to GitHub) |
| `README.md` | This guide |

## Examples of expected terminal interaction

```
Welcome to My To-Do List!

==== MY TO-DO LIST ====
1. View tasks
2. Add a task
3. Mark a task as completed
4. Delete a task
5. Exit

Choose an option (1-5): 2
Enter the task description: buy milk
Task added with ID 1.

Choose an option (1-5): 1

--- MY TASKS ---
[1] buy milk - pending

Choose an option (1-5): 3
Enter the ID of the task to complete: 1
Task 1 marked as completed.

Choose an option (1-5): 5
Goodbye! Your tasks are saved.
```

Invalid input looks like this (no crash, just a message):

```
Choose an option (1-5): 9
Invalid choice. Please enter a number from 1 to 5.

Enter the ID of the task to complete: hello
That is not a number. Please enter a task ID like 3.
```

## How task persistence works

- Every task is a dictionary: `{"id": 1, "description": "buy milk", "done": False}`
- All tasks live in one Python list.
- After every change (add, complete, delete) the whole list is written to
  `tasks.json` using `json.dump()`.
- When the app starts, `json.load()` reads the file back into the list.
- If the file is missing (first run) the app starts with an empty list.
- If the file is corrupt, it is renamed to `tasks.json.corrupt` (nothing is
  erased) and the app starts empty.

## How to run the tests

```
cd todo-app
python -m unittest discover -s tests -v
```

The tests use a temporary folder for their files, so your real
`tasks.json` is never touched.
