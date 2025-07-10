from pymongo import MongoClient
from django.conf import settings


client = MongoClient(settings.MONGO_URI)
db = client["pathnova"]  
student_profiles_collection = db["profiles"]
courses_collection = db["courses"]
