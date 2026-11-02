
import os

from storage import save_tasks, load_tasks


def test_save_and_load_tasks(tmp_path, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmp_path)

    tasks = {
        1: {
            "id": 1,
            "title": "Study Python",
            "status": "pending"
        }
    }

    # Act
    save_tasks(tasks)
    loaded_tasks = load_tasks()

    # Assert
    assert (tmp_path / "tasks.json").exists()
    assert loaded_tasks == tasks


def test_load_tasks_missing_file(tmp_path, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmp_path)

    # Act
    result = load_tasks()

    # Assert
    assert result == {}
