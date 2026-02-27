import json
import os
import sys
import tempfile
import pytest
from datetime import datetime
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import task_cli


# -------------------------
# FIXTURE: temporary file: to use this instead of tasks.json and hurting the database.
# -------------------------
@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "tasks.json"
    monkeypatch.setattr(task_cli, "TASKS_FILE", str(temp_file))
    return temp_file


# -------------------------
# TEST load_tasks()
# -------------------------
def test_load_tasks_empty_file(temp_tasks_file):
    assert task_cli.load_tasks() == []


def test_load_tasks_valid_json(temp_tasks_file):
    data = [{"id": 1, "description": "Test", "status": "todo"}]
    temp_tasks_file.write_text(json.dumps(data))
    loaded = task_cli.load_tasks()
    assert loaded == data


def test_load_tasks_corrupted_json(temp_tasks_file):
    temp_tasks_file.write_text("INVALID JSON")
    assert task_cli.load_tasks() == []


# -------------------------
# TEST save_tasks()
# -------------------------
def test_save_tasks_writes_file(temp_tasks_file):
    data = [{"id": 1, "description": "Test", "status": "todo"}]
    task_cli.save_tasks(data)

    with open(temp_tasks_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data


def test_save_tasks_permission_error(capsys):
    # Mock 'open' to raise a PermissionError when called
    with patch("builtins.open", side_effect=PermissionError):
        # We pass dummy data; the content doesn't matter because open() will fail
        task_cli.save_tasks([])

    # Capture the print output
    captured = capsys.readouterr()
    assert "Error: Could not write to tasks.json" in captured.out


def test_save_tasks_unexpected_error(capsys):
    # Mock 'open' to raise a generic Exception
    with patch("builtins.open", side_effect=Exception("Database locked")):
        task_cli.save_tasks([])

    captured = capsys.readouterr()
    assert "An unexpected error occurred" in captured.out
    assert "Database locked" in captured.out


# -------------------------
# TEST add command
# -------------------------
def test_add_command_creates_task(temp_tasks_file, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["task_cli.py", "add", "My Task"])
    task_cli.main()

    tasks = task_cli.load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "My Task"
    assert tasks[0]["status"] == "todo"


# -------------------------
# TEST update command
# -------------------------
def test_update_command_updates_description(temp_tasks_file, monkeypatch):
    task_cli.save_tasks(
        [
            {
                "id": 1,
                "description": "Old",
                "status": "todo",
                "createdAt": "2024",
                "updatedAt": "2024",
            }
        ]
    )

    monkeypatch.setattr(sys, "argv", ["task_cli.py", "update", "1", "New Task"])
    task_cli.main()

    tasks = task_cli.load_tasks()
    assert tasks[0]["description"] == "New Task"


# -------------------------
# TEST delete command
# -------------------------
def test_delete_command_removes_task(temp_tasks_file, monkeypatch):
    task_cli.save_tasks(
        [
            {
                "id": 1,
                "description": "Task",
                "status": "todo",
                "createdAt": "x",
                "updatedAt": "x",
            }
        ]
    )

    monkeypatch.setattr(sys, "argv", ["task_cli.py", "delete", "1"])
    task_cli.main()

    tasks = task_cli.load_tasks()
    assert tasks == []


# -------------------------
# TEST mark-done
# -------------------------
def test_mark_done_changes_status(temp_tasks_file, monkeypatch):
    task_cli.save_tasks(
        [
            {
                "id": 1,
                "description": "Task",
                "status": "todo",
                "createdAt": "x",
                "updatedAt": "x",
            }
        ]
    )

    monkeypatch.setattr(sys, "argv", ["task_cli.py", "mark-done", "1"])
    task_cli.main()

    tasks = task_cli.load_tasks()
    assert tasks[0]["status"] == "done"


# -------------------------
# TEST stats
# -------------------------
def test_stats_counts_correctly(temp_tasks_file, monkeypatch, capsys):
    task_cli.save_tasks(
        [
            {
                "id": 1,
                "description": "A",
                "status": "todo",
                "createdAt": "x",
                "updatedAt": "x",
            },
            {
                "id": 2,
                "description": "B",
                "status": "done",
                "createdAt": "x",
                "updatedAt": "x",
            },
        ]
    )

    monkeypatch.setattr(sys, "argv", ["task_cli.py", "stats"])
    task_cli.main()

    captured = capsys.readouterr()
    assert "Todo:" in captured.out
    assert "Done:" in captured.out


# -------------------------
# TEST list filter invalid
# -------------------------
def test_list_invalid_filter(temp_tasks_file, monkeypatch, capsys):
    task_cli.save_tasks(
        [
            {
                "id": 1,
                "description": "A",
                "status": "todo",
                "createdAt": "x",
                "updatedAt": "x",
            },
        ]
    )

    monkeypatch.setattr(sys, "argv", ["task_cli.py", "list", "invalid"])
    task_cli.main()

    captured = capsys.readouterr()
    assert "not a valid status" in captured.out


# -------------------------
# TEST list show help
# -------------------------
def test_show_help(capsys):
    task_cli.show_help()
    # capture the output
    captured = capsys.readouterr()

    # verify the key parts of the help menu are printed, this is better instead of getting the whole thing, because maybe we add something later
    assert "Task Tracker CLI Help" in captured.out
    assert "MANAGING TASKS" in captured.out
    assert "add [description]" in captured.out
    assert "help                    - Show this menu" in captured.out


def test_main_calls_show_help(monkeypatch):
    # first we patch chow help
    with patch("task_cli.show_help") as mock_show_help:

        # pretend that user wants to get help
        monkeypatch.setattr(sys, "argv", ["task_cli.py", "help"])
        task_cli.main()

        # verify the function was called exactly one time
        mock_show_help.assert_called_once()


# ---------------------------
# Test if user typed anything
# ---------------------------
def test_main_no_arguments(monkeypatch, capsys):
    # Simulate running: python task_cli.py
    monkeypatch.setattr(sys, "argv", ["task_cli.py"])

    # Patch show_help to verify it gets called
    with patch("task_cli.show_help") as mock_show_help:
        task_cli.main()

        # 3. Assert the print statement happened
        captured = capsys.readouterr()
        assert "You should tell me what to do." in captured.out

        # 4. Assert that show_help was triggered as a result
        mock_show_help.assert_called_once()


# ---------------------------
# Test if user typed anything after the name of the program
# ---------------------------
def test_main_add_missing_description(monkeypatch, capsys):
    # len(sys.argv) is 2, so it triggers your 'if len(sys.argv) < 3' check
    monkeypatch.setattr(sys, "argv", ["task_cli.py", "add"])

    # Act: Run the main function
    task_cli.main()

    # Capture the output to ensure the user got the right error
    captured = capsys.readouterr()
    assert "Error: Please provide a task description" in captured.out
    assert "Usage: python task_cli.py add" in captured.out


# ---------------------------
# Test if user typed anything afte update command
# ---------------------------
def test_main_update_missing_args(monkeypatch, capsys):
    # len(sys.argv) is 3, which is < 4, so it should trigger the error
    monkeypatch.setattr(sys, "argv", ["task_cli.py", "update", "1"])

    # Run the main function
    task_cli.main()

    # Verify the user got the error message and usage info
    captured = capsys.readouterr()
    assert "Error: Missing ID or new description." in captured.out
    assert "Usage: task-cli update [id] [new description]" in captured.out


# ---------------------------
# Test if user typed gave wrong ID after update command
# ---------------------------
def test_main_task_not_found(temp_tasks_file, monkeypatch, capsys):
    # Arrange: Create a file with only task ID 1
    task_cli.save_tasks([{"id": 1, "description": "Existing Task", "status": "todo"}])

    # Act: Try to update/delete/mark a non-existent ID (999)
    # We use 'mark-done' as an example command here
    monkeypatch.setattr(sys, "argv", ["task_cli.py", "mark-done", "999"])
    task_cli.main()

    # Assert: Capture the output to ensure the error message appears
    captured = capsys.readouterr()
    assert "Error: Task 999 not found. find the correct task ID by running 'list'"


# ---------------------------
# Test if user typed gave something but and ID
# ---------------------------
def test_main_update_invalid_id_type(monkeypatch, capsys):
    # 1. Arrange: Simulate user providing 'abc' instead of a numeric ID
    monkeypatch.setattr(
        sys, "argv", ["task_cli.py", "update", "abc", "New Description"]
    )

    # 2. Act: Run the main function
    task_cli.main()

    # 3. Assert: Capture the output to ensure the error message appears
    captured = capsys.readouterr()
    assert "Error: Task ID must be a number." in captured.out
