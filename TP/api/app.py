import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

users_file = "users.json"

class User(BaseModel):
    username: str
    password: str
    tasks: List[dict] = []

class Task(BaseModel):
    name: str
    description: Optional[str] = None
    priority: int

def load_users() -> List[User]:
    try:
        with open(users_file, "r") as f:
            users = [User(**user) for user in json.load(f)]
            print("Loaded users:", users)
            return users
    except FileNotFoundError:
        return []

def save_users(users: List[User]):
    with open(users_file, "w") as f:
        json.dump([user.dict() for user in users], f, indent=4)

# Middleware pour obtenir l'utilisateur authentifié
def get_current_user(username: str):
    users = load_users()
    user = next((u for u in users if u.username.lower() == username.lower()), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", status_code=201)
def create_user(user: User):
    users = load_users()
    if any(existing_user.username == user.username for existing_user in users):
        return {"username": user.username, "todo_count": len([])}

    users.append(user)
    save_users(users)
    return {"username": user.username, "todo_count": len(user.tasks)}

@app.post("/users/me/todo", response_model=Task, status_code=201)
def add_todo_for_user(task: Task):  # Assurez-vous de passer l'utilisateur dans la requête
    user = get_current_user("Daron")
    user.tasks.append(task.dict())
    save_users(load_users())  # Enregistrer les utilisateurs après ajout de la tâche
    return task

@app.get("/users/me/todos", response_model=List[Task])
def get_todos_for_user():
    user = get_current_user("Daron")
    return user.tasks

@app.get("/", status_code=200)
async def root():
    return {}

@app.get("/miscellaneous/addition/")
async def read_item(a: int = 0, b: int = 10):
    result = a + b
    return {"result": result}
