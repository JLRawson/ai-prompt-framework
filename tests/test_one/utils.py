from task import Task
import datetime
import json


def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def print_task(task):
    print(f"Task ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description}")
    print(f"Due Date: {task.due_date.strftime('%Y-%m-%d')}")
    print(f"Completed: {task.completed}")

def load_tasks_from_file(filename):
    with open(filename, 'r') as file:
        tasks = json.load(file)
        return [Task.from_dict(task) for task in tasks]

def save_tasks_to_file(tasks, filename):
    with open(filename, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)