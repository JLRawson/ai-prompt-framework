import json
from datetime import datetime
from task import Task

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                task.complete()

    def save_to_file(self, filename: str):
        with open(filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def load_from_file(self, filename: str):
        with open(filename, 'r') as file:
            tasks = json.load(file)
            self.tasks = [Task.from_dict(task) for task in tasks]

    def list_tasks(self):
        for task in self.tasks:
            print(task)

if __name__ == "__main__":
    todo_list = ToDoList()

    while True:
        print("\nTo-Do List Menu:")
        print("1. Add task")
        print("2. Remove task")
        print("3. Complete task")
        print("4. List tasks")
        print("5. Save to file")
        print("6. Load from file")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            task = Task(title, description, datetime.strptime(due_date, '%Y-%m-%d'))
            todo_list.add_task(task)

        elif choice == '2':
            task_id = int(input("Enter task ID to remove: "))
            todo_list.remove_task(task_id)

        elif choice == '3':
            task_id = int(input("Enter task ID to complete: "))
            todo_list.complete_task(task_id)

        elif choice == '4':
            todo_list.list_tasks()

        elif choice == '5':
            filename = input("Enter filename to save: ")
            todo_list.save_to_file(filename)

        elif choice == '6':
            filename = input("Enter filename to load: ")
            todo_list.load_from_file(filename)

        elif choice == '7':
            break

        else:
            print("Invalid choice. Please try again.")