import sys
import json
import os
from datetime import datetime


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
        print(f"adding task: {description}")
        # I will add Json save later here

    elif command == "update":
        # Update needs ID and a new description
        if len(sys.argv) < 4:
            print("Usage: task-cli update [id] [new description]")
            return
        try:
            task_id = int(sys.argv[2])

            new_description = " ".join(sys.argv[3:])
            print(f"task {task_id} updated to: {new_description}")

        except ValueError:
            print("Error: Task ID must be a number.")
            return

    elif command == "delete":
        # delete needs ID
        if len(sys.argv) < 3:
            print("Usage: task-cli delete [id]")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number.")
            return
        print(f"task {task_id} deleted")

    elif command == "mark-in-progress":
        # Update the task status
        if len(sys.argv) < 3:
            print(f"Usage: task-cli mark-in-progress [id]")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number.")
            return
        task_status = "in-progress"
        print(f"task {task_id} updated to {task_status}")

    elif command == "mark-done":
        # Update the task status to DOne
        if len(sys.argv) < 3:
            print(f"Usage: task-cli mark-done [id]")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number.")
            return
        task_status = "done"
        print(f"task {task_id} is {task_status}")

    elif command == "list":
        # List shows all the tasks or shows the done tasks or shows the in-progress tasks or todo
        if len(sys.argv) > 2:
            status_filter = sys.argv[2].lower()
            print(f"listing tasks with status: {status_filter}")
        else:
            print("listing all tasks")

    else:
        print(
            "these are the list of commands you can use:\n add, update, delete, mark-in-progress,"
            " mark-done, list, list done, list todo, list in-progress\n write 'task-cli [command] to check the usage"
        )


if __name__ == "__main__":
    main()
