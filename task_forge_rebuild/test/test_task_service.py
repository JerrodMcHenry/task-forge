
from task_service import create_task, complete_task, delete_task


def test_create_task():
    tasks = {}

    result = create_task(tasks, 1, "Study Python")

    assert result["id"] == 1
    assert result["title"] == "Study Python"
    assert result["status"] == "pending"
    assert tasks[1] == result


def test_complete_task():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"}
    }

    result = complete_task(tasks, 1)

    assert result is True
    assert tasks[1]["status"] == "completed"


def test_delete_task():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"}
    }

    result = delete_task(tasks, 1)

    assert result is True
    assert 1 not in tasks

def test_complete_nonexistent_task():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"}
    }

    result = complete_task(tasks, 99)

    assert result is False
    assert tasks[1]["status"] == "pending"


def test_delete_nonexistent_task():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"}
    }

    result = delete_task(tasks, 99)

    assert result is False
    assert 1 in tasks
    assert len(tasks) == 1