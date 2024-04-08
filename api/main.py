from fastapi import FastAPI, File, Path, UploadFile , HTTPException
import os
from typing import List
from api.models import FileUpload, PredictionRequest, PredictionResponse
import sys
# Add the directory containing the 'image_processing.py' module to sys.path 
image_processing_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(image_processing_dir)

from utils.image_processing import detect_cellphone_in_image


app = FastAPI()

# Define directory to temporarily store uploaded files
UPLOAD_TEMP_DIR = "temp_uploads"
os.makedirs(UPLOAD_TEMP_DIR, exist_ok=True)
predictions = {}

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

        # Store the prediction in the dictionary
        predictions[file.filename] = prediction_str

        return {"file_id": file.filename, "prediction": prediction_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/images/")
async def get_images_with_predictions() -> List[PredictionResponse]:
    """
    Retrieves a list of all images filenames with their predictions.

    Returns:
        List[PredictionResponse]: A list of PredictionResponse objects containing filenames and predictions.
    """
    try:
        images_with_predictions = []
        for filename, prediction in predictions.items():
            images_with_predictions.append(PredictionResponse(filename=filename, prediction=prediction))
        return images_with_predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
 # Run the FastAPI application using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

