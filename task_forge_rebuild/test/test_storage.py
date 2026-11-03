
import os
import pytest
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




def test_load_tasks_corrupted_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    corrupted_file = tmp_path / "tasks.json"
    corrupted_file.write_text('{"1": invalid}', encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="contains invalid JSON"
    ):
        load_tasks()

    assert corrupted_file.read_text(encoding="utf-8") == '{"1": invalid}'
    

def test_load_tasks_invalid_id(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    file = tmp_path / "tasks.json"
    original = '{"abc": {"id": 1, "title": "Study Python", "status": "pending"}}'
    file.write_text(original, encoding="utf-8")

    with pytest.raises(ValueError, match="task ID"):
        load_tasks()

    assert file.read_text(encoding="utf-8") == original