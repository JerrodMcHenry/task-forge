import json


def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
    

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)
            
        tasks = {}
        
        for key, value in data.items():
            tasks[int(key)] = value
            
        return tasks
    
    
    except FileNotFoundError:
        return {}