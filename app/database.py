from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["smart_todo_db"]

user_collection = db["users"]
task_collection = db["tasks"]
