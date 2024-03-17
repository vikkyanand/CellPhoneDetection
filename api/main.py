from fastapi import FastAPI, File, UploadFile
import sys
sys.path.append('f:/assignment tescra/ML_assignment\CellPhoneDetection') 
#sys.path.append('f:/assignment tescra/ml/assignment') 
app = FastAPI()
from utils.image_processing import detect_cellphone_in_image

from pymongo import MongoClient
app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["uploads"]
collection = db["images"]

@app.post("/detect-cellphone/")
async def detect_cellphone_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    result = detect_cellphone_in_image(contents)
    
    # Store the uploaded item in MongoDB
    inserted_id = collection.insert_one({"filename": file.filename, "result": result}).inserted_id
    
    return {"result": result, "uploaded_item_id": str(inserted_id)}

@app.get("/uploaded-items/")
async def get_uploaded_items():
    # Retrieve all uploaded items from MongoDB
    uploaded_items = list(collection.find({}, {"_id": 0}))
    return uploaded_items
