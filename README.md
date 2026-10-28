# To-Do List CLI (JSON) — Day 5

A beginner-friendly command-line to-do list in pure Python. Tasks are
saved to a `todos.json` file, so your list survives between runs — no
database, no setup, just the standard library.

## Features

- Add, list, complete, and delete tasks
- Tasks persist in `todos.json` (created automatically)
- `clear-done` removes all completed tasks at once
- Interactive menu mode or one-shot commands
- Safe with corrupt or hand-edited JSON files — it starts empty instead of crashing

## How to run

Requires Python 3.8+ — no third-party packages needed.

**Interactive mode** (a menu prompt):

```bash
python todo.py
```

```
> add Buy groceries
Added task #1: Buy groceries
> list
1. [ ] Buy groceries
> done 1
Done: Buy groceries
> quit
```

**One-shot commands:**

```bash
python todo.py add "Buy groceries"
python todo.py list
python todo.py done 1
python todo.py delete 2
python todo.py clear-done
```

Use a different task file with `--file`:

```bash
python todo.py --file work-tasks.json add "Finish report"
```

## Run the tests

```bash
python -m unittest test_todo -v
```

## What you learn

- **CRUD operations** — create, read, update, delete on a real data store
- **File persistence** — saving and loading state with `json` and `os.path`
- **Defensive coding** — handling missing or corrupt files gracefully
- **CLI design** — `argparse` subcommands plus an interactive loop
- **Unit testing** — testing file-backed code safely with temp directories

## Project structure

```
todo.py        # the app (task logic + CLI)
test_todo.py   # 14 unit tests
.gitignore     # keeps todos.json out of the repo
```

Part of the [Daily AI & CS Mini Projects](https://github.com/imran-shar) series — Day 5 of 30, beginner level.
