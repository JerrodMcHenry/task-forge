
def create_task(tasks, task_id, title):
    task = {
        "id": task_id,
        "title": title,
        "status": "pending"
    }

    tasks[task_id] = task
    return task


def complete_task(tasks, task_id):
    if task_id not in tasks:
        return False

    tasks[task_id]["status"] = "completed"
    return True


def delete_task(tasks, task_id):
    if task_id not in tasks:
        return False

    del tasks[task_id]
    return True

