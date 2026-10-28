"""To-Do List CLI — tasks saved to a JSON file.

Usage (interactive menu):
    python todo.py

Usage (one-shot commands):
    python todo.py add "Buy groceries"
    python todo.py list
    python todo.py done 1
    python todo.py delete 2
    python todo.py clear-done

All tasks are stored in todos.json next to this script (or in the
path given by --file). The file is created automatically on first use.
"""

import argparse
import json
import os
import sys

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")


class TodoList:
    """A small task list backed by a JSON file."""

    def __init__(self, path=DEFAULT_FILE):
        self.path = path
        self.tasks = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        # Keep only well-formed tasks so a hand-edited file can't crash us.
        tasks = []
        for item in data:
            if isinstance(item, dict) and isinstance(item.get("title"), str):
                tasks.append({"title": item["title"], "done": bool(item.get("done", False))})
        return tasks

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    def add(self, title):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        self.tasks.append({"title": title, "done": False})
        self._save()
        return len(self.tasks)  # 1-based id of the new task

    def list_tasks(self, show_done=True):
        return [(i + 1, t) for i, t in enumerate(self.tasks)
                if show_done or not t["done"]]

    def mark_done(self, task_id):
        task = self._get(task_id)
        task["done"] = True
        self._save()
        return task

    def delete(self, task_id):
        task = self._get(task_id)
        del self.tasks[task_id - 1]
        self._save()
        return task

    def clear_done(self):
        removed = sum(1 for t in self.tasks if t["done"])
        self.tasks = [t for t in self.tasks if not t["done"]]
        self._save()
        return removed

    def _get(self, task_id):
        if not isinstance(task_id, int) or task_id < 1 or task_id > len(self.tasks):
            raise IndexError(f"No task with id {task_id}.")
        return self.tasks[task_id - 1]


def format_tasks(pairs):
    if not pairs:
        return "No tasks yet. Add one with: python todo.py add \"Your task\""
    lines = []
    for task_id, task in pairs:
        box = "[x]" if task["done"] else "[ ]"
        lines.append(f"{task_id}. {box} {task['title']}")
    return "\n".join(lines)


def run_interactive(todo):
    print("To-Do List CLI  (type 'help' for commands, 'quit' to exit)")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        if not raw:
            continue
        parts = raw.split(maxsplit=1)
        cmd, arg = parts[0].lower(), (parts[1] if len(parts) > 1 else "")
        try:
            if cmd in ("quit", "exit"):
                print("Goodbye!")
                return
            elif cmd == "help":
                print("  add <title>   add a task\n"
                      "  list          show all tasks\n"
                      "  done <id>     mark a task done\n"
                      "  delete <id>   delete a task\n"
                      "  clear-done    remove all done tasks\n"
                      "  quit          exit")
            elif cmd == "add":
                print(f"Added task #{todo.add(arg)}: {arg.strip()}")
            elif cmd == "list":
                print(format_tasks(todo.list_tasks()))
            elif cmd == "done":
                task = todo.mark_done(int(arg))
                print(f"Done: {task['title']}")
            elif cmd == "delete":
                task = todo.delete(int(arg))
                print(f"Deleted: {task['title']}")
            elif cmd == "clear-done":
                print(f"Removed {todo.clear_done()} completed task(s).")
            else:
                print(f"Unknown command: {cmd} (type 'help')")
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="To-Do List CLI (tasks saved to JSON).")
    parser.add_argument("--file", default=DEFAULT_FILE, help="path to the JSON task file")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title", help="task title")
    sub.add_parser("list", help="list tasks")
    p_done = sub.add_parser("done", help="mark a task done")
    p_done.add_argument("id", type=int, help="task number from list")
    p_del = sub.add_parser("delete", help="delete a task")
    p_del.add_argument("id", type=int, help="task number from list")
    sub.add_parser("clear-done", help="remove all completed tasks")

    args = parser.parse_args(argv)
    todo = TodoList(args.file)

    if args.command is None:
        run_interactive(todo)
        return 0
    try:
        if args.command == "add":
            print(f"Added task #{todo.add(args.title)}: {args.title.strip()}")
        elif args.command == "list":
            print(format_tasks(todo.list_tasks()))
        elif args.command == "done":
            task = todo.mark_done(args.id)
            print(f"Done: {task['title']}")
        elif args.command == "delete":
            task = todo.delete(args.id)
            print(f"Deleted: {task['title']}")
        elif args.command == "clear-done":
            print(f"Removed {todo.clear_done()} completed task(s).")
    except (ValueError, IndexError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
