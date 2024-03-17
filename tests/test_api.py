from fastapi.testclient import TestClient
import sys
sys.path.append('f:/assignment tescra/ML_assignment\CellPhoneDetection') 
from api.main import app

client = TestClient(app)

def test_detect_cellphone_endpoint():
    # You can write tests for your API endpoints here
    pass
