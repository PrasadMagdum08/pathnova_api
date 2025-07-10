from pymongo import MongoClient
from pathnova_api.settings import MONGO_URI


client = MongoClient(MONGO_URI)
db = client["pathnova"]  
student_profiles_collection = db["profiles"]
courses_collection = db["courses"]
