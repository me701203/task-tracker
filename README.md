# Task Tracker CLI

A simple Command Line Interface (CLI) application to manage your tasks, track their status, and persist data using a JSON file. This project was built to practice Python fundamentals, file I/O, and JSON handling.

## Features
- **Add** new tasks with a description.
- **Update** existing task descriptions.
- **Delete** tasks by ID.
- **Mark** tasks as `todo`, `in-progress`, or `done`.
- **List** all tasks or filter them by status.
- **Advanced Sorting**: View tasks by most recently updated using `list recent`.
- **Productiviy Stats**: Get a quick summary of your task counts with `stats` command.
- **Data Persistence**: All tasks are saved in a `tasks.json` file.

## Getting Started

To use this project on your own machine, follow these steps:

0. **Clone the repository:**
```bash
git clone https://github.com/me701203/task-tracker.git
cd task-tracker
```

## How to Use
# 1. Add a Task
```bash
python task_cli.py add "Buy groceries"
```

# 2. Update a task description
```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
```
# 3. Delete a task
```bash
python task_cli.py delete 1
```

# 4. Mark a task as todo, in-progress, or done
```bash
python task_cli.py mark-todo 1
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1
```

# 5. List all tasks
```bash
python task_cli.py list
```

# 6. List tasks by status
```bash
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

# 7. Sort by recent activity
```bash
python task_cli.py list recent
```

# 8. View your progress
```bash
python task_cli.py stats
```

# 9. Maintenance (clear done tasks)
> **⚠️ WARNING:** This command will permanently remove all tasks marked as `done` from your storage. The app will ask for a `(y/n)` confirmation before proceeding.
```bash
python task_cli.py clear-done
```

## Error Handling
- **Invalid IDs**: The app checks if a task ID exists before trying to update or delete it.

- **File Safety**: Uses with blocks and try-except to prevent data corruption if the JSON file is missing or busy.

- **Empty States**: If you have no tasks, the app provides a friendly welcome message and instructions on how to start.

# Technical Details

- Language: Python 3

- Storage: JSON (tasks.json)

- Character Support: UTF-8 (supports Persian/Farsi and other scripts)