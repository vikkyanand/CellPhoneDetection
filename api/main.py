from fastapi import FastAPI, File, UploadFile , HTTPException
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
fs = GridFS(db)

# Define directory to temporarily store uploaded files
UPLOAD_TEMP_DIR = "temp_uploads"
os.makedirs(UPLOAD_TEMP_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary directory
    file_path = os.path.join(UPLOAD_TEMP_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Open the file and store it in GridFS
    with open(file_path, "rb") as f:
        file_id = fs.put(f, filename=file.filename)
    
    # Remove the temporary file
    os.remove(file_path)

    # Perform prediction
    contents = fs.get(file_id).read()
    result = detect_cellphone_in_image(contents)

    return {"file_id": str(file_id), "prediction": result}

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    # Check if file exists in GridFS
    if not fs.exists({"_id": file_id}):
        raise HTTPException(status_code=404, detail="File not found")

    # Retrieve the file from GridFS
    file = fs.get(file_id)

    # Return the file as response
    return {"filename": file.filename, "content": file.read()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)