import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    # Checking if the JSON file exists
    if not os.path.exists(TASKS_FILE):
        return []

    # using "with" so the file closes immidiately after
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)

        except json.JSONDecodeError:
            # for when the file is empty or corrupted
            return []


def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except PermissionError:
        print(
            "\nError: Could not write to tasks.json. Is the file open in another program or read-only?"
        )
    except Exception as e:
        print(f"\nAn unexpected error occurred while saving: {e}")


def show_help():
    print("\n--- Task Tracker CLI Help ---")
    print("Usage: python task_cli.py [command] [arguments]")

    print("\n VIEWING TASKS")
    print("  list                    - Display all tasks by their ID (Oldest first)")
    print("  list [status]           - Filter by: todo, in-progress, or done")
    print(
        "  list recent             - View all tasks sorted by the last time they were changed"
    )

    print("\n  MANAGING TASKS")
    print(
        "  add [description]       - Create a new task (automatically sets to 'todo')"
    )
    print("  update [id] [text]      - Change the description of an existing task")
    print("  delete [id]             - Permanently remove a task from your list")

    print("\n UPDATING STATUS")
    print("  mark-todo [id]          - Move a task back to the 'todo' list")
    print("  mark-in-progress [id]   - Mark a task as currently being worked on")
    print("  mark-done [id]          - Complete a task (Great job!)")

    print("\n MAINTENANCE")
    print("  clear-done              - Remove all 'done' tasks to keep your file clean")
    print("  stats                   - Show a summary of your productivity")
    print("  help                    - Show this menu")
    print("-" * 40)


def main():
    # --- FIRST TIME WELCOME ---
    if not os.path.exists(TASKS_FILE):
        print("🌟 Welcome to Task Tracker CLI! 🌟")
        print("It looks like this is your first time running the app.")
        print(
            "I've created a new storage file for you. Type 'python task_cli.py help' if you ever felt lost!"
        )
        print("-" * 40)
        # We create an empty file immediately so this message only shows once
        save_tasks([])

    # 1. Check if the user typed anything at all
    if len(sys.argv) < 2:
        print("You should tell me what to do.")
        show_help()
        return

    # 2. Capture the main command (add, update, delete, etc.)
    command = sys.argv[1].lower()

    if command == "add":
        # Check if user provided a task name
        if len(sys.argv) < 3:
            print("Error: Please provide a task description")
            print('Usage: python task_cli.py add "Your task description here"')
            return

        description = " ".join(sys.argv[2:])

        # load existing data
        tasks = load_tasks()

        # generate new ID, using tasks[-1] so it goes to the end of the list and then getting the real latest ID, after that we add one to prevent identical IDs
        if not tasks:
            new_id = 1
        else:
            new_id = tasks[-1]["id"] + 1

        print(f"adding task: {description}")

        # saving th current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # creating the task dictionary
        new_task = {
            "id": new_id,
            "description": description,
            "status": "todo",
            "createdAt": current_time,
            "updatedAt": current_time,
        }

        # append and save
        tasks.append(new_task)
        save_tasks(tasks)

        print(f"Task added successfuly (ID: {new_id})")

    elif command == "update":
        # Update needs ID and a new description
        if len(sys.argv) < 4:
            print("Error: Missing ID or new description.")
            print("Usage: task-cli update [id] [new description]")
            return
        try:
            task_id = int(sys.argv[2])
            # joining other argvs as the new description
            new_description = " ".join(sys.argv[3:])

            tasks = load_tasks()
            found = False

            for task in tasks:
                if task["id"] == task_id:
                    # update the description
                    task["description"] = new_description
                    # Update the time
                    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    found = True
                    break  # We found it, so get out of the loop

            if found:
                save_tasks(tasks)
                print(f"task {task_id} updated to: {new_description}")
            else:
                print(
                    f"Error: Task {task_id} not found. find the correct task ID by running 'list'"
                )

        except ValueError:
            print("Error: Task ID must be a number.")
            return

    elif command == "delete":
        tasks = load_tasks()

        # delete needs ID
        if len(sys.argv) < 3:
            print("Error: Missing Task ID.")
            print("Usage: task-cli.py delete [id]")
            return
        try:
            task_id = int(sys.argv[2])

            original_count = len(tasks)
            new_tasks = []

            for task in tasks:
                if task["id"] != task_id:
                    new_tasks.append(task)

            tasks = new_tasks

            # Check if we actually removed any task
            if len(tasks) < original_count:
                save_tasks(tasks)
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Error: Task with ID {task_id} not found.")

        except ValueError:
            print("Error: Task ID must be a number.")
            return

        # print(f"task {task_id} deleted")

    elif command == "mark-in-progress":
        # Update the task status
        if len(sys.argv) < 3:
            print("Error: you need to provide and ID.")
            print("Usage: task-cli.py mark-in-progress [id]")
            return

        try:
            task_id = int(sys.argv[2])
            tasks = load_tasks()
            found = False

            for task in tasks:
                if task["id"] == task_id:
                    # update the status
                    task["status"] = "in-progress"
                    # update the time
                    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    found = True
                    break  # we found the task needed updating

            if found:
                save_tasks(tasks)
                print(f"task {task_id} updated to 'in-progress'")
            else:
                print(
                    f"Error: Task {task_id} not found. try getting the right ID by 'list' command"
                )

        except ValueError:
            print("Error: Task ID must be a number.")
            return

    elif command == "mark-done":
        # Update the task status to DOne
        if len(sys.argv) < 3:
            print("Error: Please Provide and ID.")
            print("Usage: task-cli mark-done [id]")
            return

        try:
            task_id = int(sys.argv[2])
            tasks = load_tasks()
            found = False

            for task in tasks:
                if task["id"] == task_id:
                    # update the status
                    task["status"] = "done"
                    # update the time
                    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    found = True
                    break  # it's found. get out.

            if found:
                save_tasks(tasks)
                print(f"Task {task_id} is now done, great job!")
            else:
                print(
                    f"Task {task_id} was not found, try getting the right ID by running 'list' "
                )
        except ValueError:
            print("Error: Task ID must be a number.")
            return

    elif command == "mark-todo":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-todo [id]")
            return

        try:
            task_id = int(sys.argv[2])
            tasks = load_tasks()
            found = False

            for task in tasks:
                if task["id"] == task_id:
                    task["status"] = "todo"
                    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    found = True
                    break

            if found:
                save_tasks(tasks)
                print(f"Task {task_id} status reset to 'todo'.")
            else:
                print(f"Error: Task {task_id} not found.")

        except ValueError:
            print("Error: Task ID must be a number.")
            return

    elif command == "list":
        tasks = load_tasks()

        if not tasks:
            print("There's Nothing Here, Consider adding a task with 'add' command")
            return

        # List shows all the tasks or shows the done tasks or shows the in-progress tasks or todo
        if len(sys.argv) > 2:
            status_filter = sys.argv[2].lower()
            # print(f"listing tasks with status: {status_filter}")
        else:
            status_filter = None
            # print("listing all tasks")

        valid_statuses = ["todo", "in-progress", "done", "recent", None]
        if status_filter not in valid_statuses:
            print(
                f"Error: '{status_filter}' is not a valid status.\nValid statuses are: todo, in-progress, done, recent"
            )
            return

        if status_filter == "recent":
            tasks.sort(key=lambda x: x["updatedAt"], reverse=True)

        # printing a header for the table
        print("\n     ID     Status               Description")
        print("-" * 50)

        for task in tasks:
            # If it's 'recent' or None, we show EVERYTHING (just in different order)
            # If it's todo/done/in-progress, we filter it
            if status_filter in [None, "recent"] or task["status"] == status_filter:
                print(
                    f"     {task['id']}      {task['status']}                 {task['description']}"
                )
        print("-" * 50)

    elif command == "help":
        # We reuse the same logic we want for the unknown commands
        show_help()

    elif command == "clear-done":
        tasks = load_tasks()

        # 1. Create a brand new empty list to hold the tasks we want to KEEP
        fresh_tasks = []

        # 2. Go through every task in our current list
        for task in tasks:
            # 3. If the task is NOT done, it stays!
            if task["status"] != "done":
                fresh_tasks.append(task)

        # 4. Check if we actually have anything to remove
        removed_count = len(tasks) - len(fresh_tasks)

        if removed_count > 0:
            # --- THE NEW CONFIRMATION QUESTION ---
            print(
                f"Warning: This will permanently delete {removed_count} 'done' tasks."
            )
            confirm = input("Are you sure you want to proceed? (y/n): ").lower()

            if confirm == "y":
                save_tasks(fresh_tasks)
                print(f"Successfully cleaned up {removed_count} completed tasks.")
            else:
                print("Action canceled. No tasks were deleted.")

        else:
            print("No completed tasks to remove.")

    # adding stats like: "You have 4 Todo, 1 In-Progress, and 12 Done."
    elif command == "stats":
        tasks = load_tasks()

        if not tasks:
            print("📊 Stats: You have no tasks yet. Add some to see progress!")
            return

        # Initialize our counters
        todo_count = 0
        in_progress_count = 0
        done_count = 0

        # Loop through and count
        for task in tasks:
            if task["status"] == "todo":
                todo_count += 1
            elif task["status"] == "in-progress":
                in_progress_count += 1
            elif task["status"] == "done":
                done_count += 1

        total = len(tasks)

        print("\n--- Task Statistics ---")
        print(f"Todo:        {todo_count}")
        print(f"In-Progress: {in_progress_count}")
        print(f"Done:        {done_count}")
        print("-" * 25)
        print(f"Total Tasks: {total}")
        print("-" * 25)

    else:
        print(f"\nError: '{command}' is not a recognized command.")
        show_help()


if __name__ == "__main__":
    main()
