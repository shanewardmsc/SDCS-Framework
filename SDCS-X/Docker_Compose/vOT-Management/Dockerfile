# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (if your Python script runs a web server, e.g., FastAPI or Flask)
EXPOSE 9970

# Command to run the application
CMD ["python", "vOT_Manager.py"]

