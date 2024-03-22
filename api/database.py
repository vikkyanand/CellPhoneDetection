from pymongo import MongoClient
from gridfs import GridFS

client = MongoClient("mongodb://localhost:27017")
db = client["uploads"]
fs = GridFS(db)