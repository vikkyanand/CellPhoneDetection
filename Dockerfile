# Use the official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the project dependencies
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /app
COPY . .

# Run the FastAPI application when the container starts
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
