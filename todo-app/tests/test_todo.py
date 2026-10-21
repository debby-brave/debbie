"""Automated tests for the to-do list app.

Run from the todo-app folder with:
    python -m unittest discover -s tests -v

The tests NEVER touch your real tasks.json file:
storage tests write to a temporary file that is deleted afterwards.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import todo
import storage


class TestAddTask(unittest.TestCase):
    """Adding tasks: validation and unique IDs."""

    def test_add_task_strips_spaces_and_saves_description(self):
        tasks = []

        task = todo.add_task(tasks, "  buy milk  ")

        self.assertEqual(task["description"], "buy milk")
        self.assertEqual(len(tasks), 1)

    def test_add_task_rejects_empty_description(self):
        tasks = []

        with self.assertRaises(ValueError):
            todo.add_task(tasks, "")

        self.assertEqual(tasks, [])  # nothing was added

    def test_add_task_rejects_spaces_only_description(self):
        tasks = []

        with self.assertRaises(ValueError):
            todo.add_task(tasks, "     ")

        self.assertEqual(tasks, [])

    def test_add_task_assigns_sequential_ids(self):
        tasks = []

        todo.add_task(tasks, "first task")
        todo.add_task(tasks, "second task")

        self.assertEqual([t["id"] for t in tasks], [1, 2])

    def test_ids_are_not_reused_after_deletion(self):
        tasks = []
        todo.add_task(tasks, "task one")
        todo.add_task(tasks, "task two")
        todo.add_task(tasks, "task three")

        todo.delete_task(tasks, 2)  # delete the middle task

        new_task = todo.add_task(tasks, "task four")

        self.assertEqual(new_task["id"], 4)  # not 2, not 3

    def test_new_task_starts_pending(self):
        tasks = []

        task = todo.add_task(tasks, "write report")

        self.assertFalse(task["done"])


class TestCompleteAndDelete(unittest.TestCase):
    """Completing and deleting: success and graceful failure."""

    def setUp(self):
        # A fresh 3-task list before every test in this class.
        self.tasks = []
        todo.add_task(self.tasks, "task one")
        todo.add_task(self.tasks, "task two")
        todo.add_task(self.tasks, "task three")

    def test_complete_task_marks_it_done(self):
        result = todo.complete_task(self.tasks, 2)

        self.assertTrue(result)
        self.assertTrue(self.tasks[1]["done"])
        # The other tasks were not touched:
        self.assertFalse(self.tasks[0]["done"])
        self.assertFalse(self.tasks[2]["done"])

    def test_complete_task_with_invalid_id_returns_false(self):
        result = todo.complete_task(self.tasks, 99)

        self.assertFalse(result)

    def test_delete_task_removes_only_that_task(self):
        result = todo.delete_task(self.tasks, 2)

        self.assertTrue(result)
        self.assertEqual(len(self.tasks), 2)
        self.assertEqual([t["description"] for t in self.tasks],
                         ["task one", "task three"])

    def test_delete_task_with_invalid_id_returns_false(self):
        result = todo.delete_task(self.tasks, 99)

        self.assertFalse(result)
        self.assertEqual(len(self.tasks), 3)

    def test_find_task_returns_none_for_missing_id(self):
        self.assertIsNone(todo.find_task(self.tasks, 99))


class TestDisplay(unittest.TestCase):
    """Displaying must not crash on edge cases."""

    def test_display_empty_list_does_not_crash(self):
        # display_tasks only prints; if it raises, the test fails.
        todo.display_tasks([])

    def test_display_list_with_tasks_does_not_crash(self):
        tasks = []
        todo.add_task(tasks, "buy bread")

        todo.display_tasks(tasks)

    def test_format_status_pending_and_completed(self):
        pending = {"id": 1, "description": "a", "done": False}
        completed = {"id": 2, "description": "b", "done": True}

        self.assertEqual(todo.format_status(pending), "pending")
        self.assertEqual(todo.format_status(completed), "completed")


class TestStorage(unittest.TestCase):
    """Saving and loading JSON, safely separated from real data."""

    def test_save_and_load_roundtrip(self):
        tasks = []
        todo.add_task(tasks, "buy milk")
        todo.complete_task(tasks, 1)
        todo.add_task(tasks, "call mum")

        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "test_tasks.json")

            storage.save_tasks(tasks, path)
            loaded = storage.load_tasks(path)

        self.assertEqual(loaded, tasks)
        self.assertEqual(loaded[0]["done"], True)

    def test_load_missing_file_returns_empty_list(self):
        # A brand-new user has no file yet; the app must still start.
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "does_not_exist.json")

            self.assertEqual(storage.load_tasks(path), [])

    def test_load_invalid_json_returns_empty_and_keeps_backup(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "broken.json")

            with open(path, "w", encoding="utf-8") as file:
                file.write("{ this is not valid json !!! ")

            loaded = storage.load_tasks(path)

            self.assertEqual(loaded, [])
            # The broken file was kept, renamed, not deleted:
            self.assertTrue(os.path.exists(path + ".corrupt"))

    def test_load_empty_file_returns_empty_list(self):
        # A 0-byte file (created but never written) is invalid JSON too.
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "empty.json")
            open(path, "w").close()

            self.assertEqual(storage.load_tasks(path), [])

    def test_load_non_list_json_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "wrong_shape.json")

            with open(path, "w", encoding="utf-8") as file:
                file.write('{"oops": "a dict, not a list"}')

            self.assertEqual(storage.load_tasks(path), [])


if __name__ == "__main__":
    unittest.main()
