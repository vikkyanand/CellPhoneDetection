from bson import ObjectId
from fastapi import FastAPI, File, Path, UploadFile , HTTPException
import os
from models import FileUpload, PredictionRequest, PredictionResponse  # Import data models
import sys
# Add the directory containing the 'image_processing.py' module to sys.path 
image_processing_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(image_processing_dir)

from image_processing import detect_cellphone_in_image


app = FastAPI()

# Connect to MongoDB
from database import db, fs

# Define directory to temporarily store uploaded files
UPLOAD_TEMP_DIR = "temp_uploads"
os.makedirs(UPLOAD_TEMP_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_and_predict(file: UploadFile = File(...)):
    """
    Uploads an image file and performs cellphone detection prediction.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        dict: A dictionary containing the file ID and prediction.
    """
    try:
        # Read the file content
        file_content = await file.read()

        # Perform prediction
        prediction = detect_cellphone_in_image(file_content)

        # Convert boolean prediction to string
        prediction_str = "Cellphone Detected" if prediction else "No Cellphone Detected"

        # Save the uploaded file content to a temporary directory
        file_path = os.path.join(UPLOAD_TEMP_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Open the file and store it in GridFS
        with open(file_path, "rb") as f:
            file_id = fs.put(f, filename=file.filename)

        # Remove the temporary file
        os.remove(file_path)

        # Save prediction in MongoDB
        prediction_collection = db["predictions"]
        prediction_collection.insert_one({
            "file_id": str(file_id),
            "filename": file.filename,
            "prediction": prediction_str  # Use the converted string prediction
        })

        return {"file_id": str(file_id), "prediction": prediction_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/images/")
async def get_images_with_predictions():
    """
    Retrieves a list of all images with their predictions.

    Returns:
        list: A list of PredictionResponse objects containing filenames and predictions.
    """

    images_with_predictions = []
    try:
    # Retrieve the prediction collection from MongoDB
        prediction_collection = db["predictions"]
        for prediction_doc in prediction_collection.find():
            # Extract the filename and prediction from the document
            filename = prediction_doc["filename"]
            prediction = prediction_doc["prediction"]
            images_with_predictions.append(PredictionResponse(filename=filename, prediction=prediction))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return images_with_predictions


@app.get("/images/{file_identifier}")
async def get_prediction(
    file_identifier: str = Path(..., description="File ID or Name"),
):
    """
    Retrieves the prediction for a specific image.

    Args:
        file_identifier (str): The file ID or name.

    Returns:
        PredictionResponse: The PredictionResponse object containing the filename and prediction.
    """
    try:
        if ObjectId.is_valid(file_identifier):
            # If the identifier is a valid ObjectId, query by file_id
            prediction_doc = db["predictions"].find_one({"file_id": ObjectId(file_identifier)})
        else:
            # If not, query by filename
            prediction_doc = db["predictions"].find_one({"filename": file_identifier})

        if prediction_doc:
            filename = prediction_doc["filename"]
            prediction = prediction_doc["prediction"]
            return PredictionResponse(filename=filename, prediction=prediction)
        else:
            raise HTTPException(status_code=404, detail="Prediction not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

 # Run the FastAPI application using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

