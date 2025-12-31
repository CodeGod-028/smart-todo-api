from fastapi import FastAPI, HTTPException, Depends
from bson import ObjectId

from app.schemas import (
    UserCreate,
    UserLogin,
    TaskCreate,
    TaskUpdate
)
from app.database import user_collection, task_collection
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

app = FastAPI(title="Smart ToDo API")

# ---------- AUTH ROUTES ----------

@app.post("/auth/register")
def register(user: UserCreate):
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    user_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password)
    })

    return {"message": "User registered successfully"}

@app.post("/auth/login")
def login(user: UserLogin):
    db_user = user_collection.find_one({"email": user.email})

    if not db_user or not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(db_user["email"])
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ---------- TASK ROUTES (PROTECTED) ----------

@app.post("/tasks")
def create_task(
    task: TaskCreate,
    user: str = Depends(get_current_user)
):
    task_collection.insert_one({
        "title": task.title,
        "description": task.description,
        "user": user
    })
    return {"message": "Task created"}

@app.get("/tasks")
def get_tasks(user: str = Depends(get_current_user)):
    tasks = []
    for t in task_collection.find({"user": user}):
        tasks.append({
            "id": str(t["_id"]),
            "title": t["title"],
            "description": t.get("description")
        })
    return tasks

@app.put("/tasks/{task_id}")
def update_task(
    task_id: str,
    task: TaskUpdate,
    user: str = Depends(get_current_user)
):
    result = task_collection.update_one(
        {"_id": ObjectId(task_id), "user": user},
        {"$set": {k: v for k, v in task.dict().items() if v is not None}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    user: str = Depends(get_current_user)
):
    result = task_collection.delete_one(
        {"_id": ObjectId(task_id), "user": user}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}
