from bson import ObjectId
from fastapi import FastAPI, File, Path, UploadFile , HTTPException
import os

import sys
sys.path.append('f:/assignment tescra/ML_assignment\CellPhoneDetection') 
from utils.image_processing import detect_cellphone_in_image

app = FastAPI()

# Connect to MongoDB
from database import db, fs

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

    contents = fs.get(file_id).read()
    prediction = detect_cellphone_in_image(contents)

    # Save prediction in MongoDB
    filename = file.filename
    prediction_collection = db["predictions"]
    prediction_collection.insert_one({"file_id": file_id, "filename": filename, "prediction": prediction})

    return {"file_id": str(file_id), "prediction": prediction}

@app.get("/images/")
async def get_images_with_predictions():
    images_with_predictions = []
    try:
        prediction_collection = db["predictions"]
        for prediction_doc in prediction_collection.find():
            file_id = prediction_doc["file_id"]
            filename = fs.get(file_id).filename
            prediction = prediction_doc["prediction"]
            images_with_predictions.append({"filename": filename, "prediction": prediction})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return images_with_predictions

@app.get("/images/{file_identifier}")
async def get_prediction(
    file_identifier: str = Path(..., description="File ID or Name"),
):
    try:
        if ObjectId.is_valid(file_identifier):
            # If the identifier is a valid ObjectId, query by file_id
            prediction_doc = db["predictions"].find_one({"file_id": ObjectId(file_identifier)})
        else:
            # If not, query by filename
            prediction_doc = db["predictions"].find_one({"filename": file_identifier})

        if prediction_doc:
            file_id = prediction_doc["file_id"]
            filename = fs.get(file_id).filename
            prediction = prediction_doc["prediction"]
            return {"filename": filename, "prediction": prediction}
        else:
            raise HTTPException(status_code=404, detail="Prediction not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#uvicorn main:app --reload