from fastapi import FastAPI, File, UploadFile
import os
from fastapi.staticfiles import StaticFiles
import sys
sys.path.append('f:/assignment tescra/ML_assignment\CellPhoneDetection') 
#sys.path.append('f:/assignment tescra/ml/assignment') 
app = FastAPI()
from utils.image_processing import detect_cellphone_in_image

from pymongo import MongoClient
from gridfs import GridFS
app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["uploads"]
collection = db["images"]

# Define directory to store uploaded images
UPLOADS_DIRECTORY = "uploads"

# Create directory if it doesn't exist
os.makedirs(UPLOADS_DIRECTORY, exist_ok=True)

# Mount directory as static files
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIRECTORY), name="uploads")

@app.post("/detect-cellphone/")
async def detect_cellphone_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    result = detect_cellphone_in_image(contents)
    
    # Save the uploaded image to the uploads directory
    file_path = os.path.join(UPLOADS_DIRECTORY, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Store metadata in MongoDB
    inserted_id = collection.insert_one({"filename": file.filename, "result": result}).inserted_id
    
    return {"result": result, "uploaded_item_id": str(inserted_id)}

@app.get("/uploaded-items/")
async def get_uploaded_items():
    # Retrieve all uploaded items from MongoDB
    uploaded_items = list(collection.find({}, {"_id": 0}))
    return uploaded_items