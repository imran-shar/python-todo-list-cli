"""Tests for the To-Do List CLI (todo.py).

Run:  python -m unittest test_todo -v
"""

import json
import os
import tempfile
import unittest

from todo import TodoList, format_tasks


class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "todos.json")
        self.todo = TodoList(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_list(self):
        self.assertEqual(self.todo.add("Buy milk"), 1)
        self.assertEqual(self.todo.add("Read book"), 2)
        pairs = self.todo.list_tasks()
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0][1]["title"], "Buy milk")
        self.assertFalse(pairs[0][1]["done"])

    def test_add_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.todo.add("   ")

    def test_persists_to_json_file(self):
        self.todo.add("Persist me")
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [{"title": "Persist me", "done": False}])

    def test_reloads_from_existing_file(self):
        self.todo.add("First")
        reloaded = TodoList(self.path)
        self.assertEqual(len(reloaded.tasks), 1)
        self.assertEqual(reloaded.tasks[0]["title"], "First")

    def test_mark_done(self):
        self.todo.add("Task A")
        task = self.todo.mark_done(1)
        self.assertTrue(task["done"])
        self.assertTrue(TodoList(self.path).tasks[0]["done"])

    def test_mark_done_invalid_id(self):
        self.todo.add("Task A")
        with self.assertRaises(IndexError):
            self.todo.mark_done(5)
        with self.assertRaises(IndexError):
            self.todo.mark_done(0)

    def test_delete(self):
        self.todo.add("Keep me")
        self.todo.add("Drop me")
        removed = self.todo.delete(2)
        self.assertEqual(removed["title"], "Drop me")
        self.assertEqual([t["title"] for t in self.todo.tasks], ["Keep me"])

    def test_delete_invalid_id(self):
        with self.assertRaises(IndexError):
            self.todo.delete(1)

    def test_clear_done_keeps_pending(self):
        self.todo.add("Done one")
        self.todo.add("Pending one")
        self.todo.mark_done(1)
        self.assertEqual(self.todo.clear_done(), 1)
        self.assertEqual([t["title"] for t in self.todo.tasks], ["Pending one"])

    def test_corrupt_file_starts_empty(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{not valid json")
        self.assertEqual(TodoList(self.path).tasks, [])

    def test_missing_file_starts_empty(self):
        self.assertEqual(TodoList(os.path.join(self.tmp.name, "nope.json")).tasks, [])

    def test_format_tasks_empty(self):
        self.assertIn("No tasks yet", format_tasks([]))

    def test_format_tasks_marks_done(self):
        self.todo.add("Done task")
        self.todo.mark_done(1)
        self.todo.add("Open task")
        out = format_tasks(self.todo.list_tasks())
        self.assertIn("1. [x] Done task", out)
        self.assertIn("2. [ ] Open task", out)

    def test_list_pending_only(self):
        self.todo.add("Done task")
        self.todo.add("Open task")
        self.todo.mark_done(1)
        pending = self.todo.list_tasks(show_done=False)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0][1]["title"], "Open task")


if __name__ == "__main__":
    unittest.main()
