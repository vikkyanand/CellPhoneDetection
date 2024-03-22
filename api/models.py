from typing import Optional
from pydantic import BaseModel

class FileUpload(BaseModel):
    byte: bytes
    name: Optional[str] = None

class PredictionRequest(BaseModel):
    file_id: str
    filename: str
    prediction: str

class PredictionResponse(BaseModel):
    filename: str
    prediction: str
