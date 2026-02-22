# Task Tracker CLI

A simple Command Line Interface (CLI) application to manage your tasks, track their status, and persist data using a JSON file. This project was built to practice Python fundamentals, file I/O, and JSON handling.

## Features
- **Add** new tasks with a description.
- **Update** existing task descriptions.
- **Delete** tasks by ID.
- **Mark** tasks as `todo`, `in-progress`, or `done`.
- **List** all tasks or filter them by status.
- **Data Persistence**: All tasks are saved in a `tasks.json` file.

## Getting Started

To use this project on your own machine, follow these steps:

1. **Clone the repository:**
```bash
git clone [https://github.com/me701203/task-tracker.git](https://github.com/me701203/task-tracker.git)
cd task-tracker

## How to Use

# Add a task
python task_cli.py add "Buy groceries"

# Update a task description
python task_cli.py update 1 "Buy groceries and cook dinner"

# Delete a task
python task_cli.py delete 1

# Update a task description
python task_cli.py update 1 "Buy groceries and cook dinner"

# Delete a task
python task_cli.py delete 1

# Mark a task as todo, in-progress, or done
python task_cli.py mark-todo 1
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1

# List all tasks
python task_cli.py list

# List tasks by status
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```
# Technical Details

Language: Python 3

Storage: JSON (tasks.json)

Character Support: UTF-8 (supports Persian/Farsi and other scripts)