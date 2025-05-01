# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Update package list and install iputils-ping
RUN apt-get update && apt-get install -y iputils-ping

# Set the working directory in the container
WORKDIR /app

# Set the environment variable for Docker socket
ENV DOCKER_HOST=unix:///var/run/docker.sock

# Copy the current directory contents into the container at /app
COPY . /app
COPY ./appdata/plc_tags.csv /app/data/plc_tags.csv

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (if your Python script runs a web server, e.g., FastAPI or Flask)
EXPOSE 9960

# Command to run the application
CMD ["python", "vIT_Manager.py"]

