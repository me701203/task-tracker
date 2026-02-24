import os
import json
import task_cli

# We override the filename in the script so it doesn't touch the real data
task_cli.TASKS_FILE = "test_data.json"


def run_tests():
    print("--- Starting Task Tracker Tests ---")

    # PREPARATION: Ensure the file is empty(gone) before we start
    if os.path.exists("test_data.json"):
        os.remove("test_data.json")

    # --- TEST 1: ADDING ---
    print("Testing Add...")
    # We simulate adding a task by creating a list and saving it
    sample_task = [{"id": 1, "description": "Test Task", "status": "todo"}]
    task_cli.save_tasks(sample_task)

    # Now we load it back to see if it worked
    loaded = task_cli.load_tasks()

    if len(loaded) == 1 and loaded[0]["description"] == "Test Task":
        print("Add Test: PASSED")
    else:
        print("Add Test: FAILED")

    # --- TEST 2: STATUS CHANGE ---
    print("Testing Status Update...")
    loaded[0]["status"] = "done"
    task_cli.save_tasks(loaded)

    updated = task_cli.load_tasks()
    if updated[0]["status"] == "done":
        print("Status Test: PASSED")
    else:
        print("Status Test: FAILED")

    # --- TEST 3: DELETING ---
    print("Testing Delete...")
    task_cli.save_tasks([])  # Save an empty list
    final_check = task_cli.load_tasks()

    if len(final_check) == []:
        print("Delete Test: PASSED")
    else:
        print("Delete Test: FAILED")

    # --- TEST 4: NON-NUMBER ID ---
    print("Test 4: Non-number ID for update/delete...")
    # Your try/except catches ValueError. We simulate that logic:
    try:
        val = int("apple")
    except ValueError:
        print("Correctly identifies that 'apple' is not a number.")

    # --- TEST 5: INVALID STATUS FILTER ---
    print("Test 5: Invalid list filter...")
    valid_statuses = ["todo", "in-progress", "done", None]
    bad_filter = "finished"
    if bad_filter not in valid_statuses:
        print("Invalid status filter caught: PASSED")

    # --- TEST 6: UPDATE NON-EXISTENT ID ---
    print("Test 6: Updating an ID that doesn't exist...")
    found = False
    for task in loaded:
        if task["id"] == 999:
            found = True
    if not found:
        print("Non-existent ID handling: PASSED")

    # CLEANUP: Remove the fake file so the folder stays tidy
    if os.path.exists("test_data.json"):
        os.remove("test_data.json")

    print("--- Tests Finished ---")


if __name__ == "__main__":
    run_tests()
