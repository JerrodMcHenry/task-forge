import json


def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
    

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError(
                "Invalid task data: expected a dictionary."
            )

        tasks = {}

        for key, value in data.items():
            try:
                task_id = int(key)
            except ValueError as error:
                raise ValueError(
                    f"Invalid task data: task ID '{key}' is not an integer."
                ) from error

            tasks[task_id] = value

        return tasks

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError as error:
        raise ValueError(
            "Cannot load tasks: tasks.json contains invalid JSON."
        ) from error