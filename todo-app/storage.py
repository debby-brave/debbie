"""Save and load the task list as a JSON file.

This file owns ONE job: talking to the disk.
The rest of the app does not know HOW tasks are stored,
it only calls load_tasks() and save_tasks().
"""


import json
import os


# Always keep the data file NEXT TO this code file, no matter
# where you run the command from (repo root or inside this folder).
DATA_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DATA_FOLDER, "tasks.json")


def load_tasks(path=DATA_FILE):
    """Read tasks from a JSON file and return them as a list of dictionaries.

    Safe for beginners to call at startup:
    - file does not exist yet  -> return [] (first run, nothing saved)
    - file has broken JSON     -> keep a copy as .corrupt and return []
    """

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            tasks = json.load(file)

    except json.JSONDecodeError:
        # The file exists but is not valid JSON.
        # Rename it instead of deleting it, so no data is lost.
        backup_path = path + ".corrupt"
        os.replace(path, backup_path)
        print(f"Warning: {path} was not valid JSON.")
        print(f"A copy was kept at {backup_path} and we start with an empty list.")
        return []

    if not isinstance(tasks, list):
        # Valid JSON, but not the shape we expect (should be a list).
        print(f"Warning: {path} does not contain a task list. Starting empty.")
        return []

    return tasks


def save_tasks(tasks, path=DATA_FILE):
    """Write the whole task list to a JSON file.

    json.dump converts Python objects into text we can read back later.
    indent=4 makes the file human-readable (4 spaces per level).
    """

    with open(path, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)
