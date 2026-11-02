
from task_service import create_task, complete_task, delete_task, update_task_title


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
    
from task_service import filter_tasks_by_status, search_tasks


def test_filter_tasks_by_status():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"},
        2: {"id": 2, "title": "Build API", "status": "completed"},
    }

    results = filter_tasks_by_status(tasks, "pending")

    assert len(results) == 1
    assert results[0]["id"] == 1


def test_search_tasks_case_insensitive():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"},
        2: {"id": 2, "title": "Build API", "status": "completed"},
    }

    results = search_tasks(tasks, "PYTHON")

    assert len(results) == 1
    assert results[0]["title"] == "Study Python"
    
    
def test_update_task_title():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"}
    }

    result = update_task_title(tasks, 1, "Practice Python")

    assert result is True
    assert tasks[1]["title"] == "Practice Python"
    assert tasks[1]["status"] == "pending"
    assert tasks[1]["id"] == 1


def test_update_task_title_invalid():
    tasks = {
        1: {"id": 1, "title": "Study Python", "status": "pending"}
    }

    assert update_task_title(tasks, 99, "New Title") is False
    assert update_task_title(tasks, 1, "   ") is False
    assert tasks[1]["title"] == "Study Python"