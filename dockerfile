# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install pkg-config and other required system packages
RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    libmariadb-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables (replace these with actual values or secrets)
ENV DB_HOST=localhost
ENV DB_USER=admin
ENV DB_PASSWORD=admin
ENV DB_NAME=WS-AI-VS

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
