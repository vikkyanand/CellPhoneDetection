# Cell Phone Detection API

This is a FastAPI-based web API for detecting cell phones in images. It allows users to upload images, make predictions, and retrieve images with predictions.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vikkyanand/CellPhoneDetection.git
```

2. Navigate to the project directory:

```bash
cd CellPhoneDetection
```

3. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Unix/Linux
venv\Scripts\activate      # On Windows
```

4. Install dependencies using pip:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
uvicorn main:app --reload
```

The FastAPI application will start running. You can access it at http://localhost:8000/docs.

## Usage

### Uploading Images and Making Predictions

To upload an image and simultaneously make predictions, send a POST request to /upload/. Include the image file as the request body. The response will include the file ID and prediction result.

Example:

```bash
curl -X POST -F "file=@image.jpg" http://localhost:8000/upload/
```

### Retrieving Images with Predictions

To retrieve images with predictions, send a GET request to /images/. This will return a list of images along with their predictions.

```bash
curl http://localhost:8000/images/
```

## Docker Setup

1. Make sure you have Docker installed on your machine. You can download and install Docker from the official Docker website.

2. Build the Docker container:

```bash
docker-compose build
```

3. Run the Docker container:

```bash
docker-compose up
```

The FastAPI application will start running in a Docker container. You can access it at http://localhost:8000/docs.

## GitHub Repository

You can find the source code for this project on [GitHub Repository](https://github.com/vikkyanand/CellPhoneDetection).
