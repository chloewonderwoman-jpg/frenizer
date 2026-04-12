import json
import os
import uuid

FILE_PATH = "todos.json"

def _ensure_file():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([], file)

def get_todos():
    _ensure_file()
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_todos(todos):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(todos, file, indent=2)

def add_todo(title, deadline):
    todos = get_todos()
    todos.append(
        {
            "id": str(uuid.uuid4()),
            "title": title,
            "deadline": deadline,
            "completed": False
        }
    )
    save_todos(todos)

def update_todo(todo_id, completed):
    todos = get_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = completed
            break
    save_todos(todos)

def delete_todo(todo_id):
    todos = get_todos()
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)