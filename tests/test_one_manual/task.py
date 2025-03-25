import json
from datetime import datetime

class Task:
    id_counter = 1

    def __init__(self, title: str, description: str, due_date: datetime):
        self.id = Task.id_counter
        Task.id_counter += 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False

    def complete(self):
        self.completed = True

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.strftime('%Y-%m-%d'),
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, task_dict):
        task = cls(
            task_dict['title'],
            task_dict['description'],
            datetime.strptime(task_dict['due_date'], '%Y-%m-%d')
        )
        task.id = task_dict['id']
        task.completed = task_dict['completed']
        return task

    def __str__(self):
        return f"Task ID: {self.id}\nTitle: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date.strftime('%Y-%m-%d')}\nCompleted: {self.completed}"