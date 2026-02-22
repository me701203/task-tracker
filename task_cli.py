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


def main():
    # 1. Check if the user typed anything at all
    if len(sys.argv) < 2:
        print("Usage: task-cli [command] [arguments]")
        return

    # 2. Capture the main command (add, update, delete, etc.)
    command = sys.argv[1].lower()

    if command == "add":
        # Check if user provided a task name
        if len(sys.argv) < 3:
            print("Error: Please provide a task description")
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
            print("Usage: task-cli delete [id]")
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
            print(f"Usage: task-cli mark-in-progress [id]")
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
            print(f"Usage: task-cli mark-done [id]")
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

        valid_statuses = ["todo", "in-progress", "done", None]
        if status_filter not in valid_statuses:
            print(
                f"Error: '{status_filter}' is not a valid status.\nValid statuses are: todo, in-progress, done"
            )
            return

        # printing a header for the table
        print("\nID     Status               Description")
        print("-" * 50)

        for task in tasks:
            # if there is no filter or if the task matches the filter, print it
            if status_filter is None or task["status"] == status_filter:
                print(
                    f"{task['id']}      {task['status']:<15}      {task['description']}"
                )
        print("-" * 50)

    else:
        print(
            "these are the list of commands you can use:\n add, update, delete, mark-in-progress,"
            " mark-done, list, list done, list todo, list in-progress\n write 'task-cli [command] to check the usage"
        )


if __name__ == "__main__":
    main()
