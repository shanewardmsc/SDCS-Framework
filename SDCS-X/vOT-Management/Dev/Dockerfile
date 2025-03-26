# Use an official Python runtime as a base
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy application files
COPY vPLC_Test.py /app/vPLC_Test.py

# Install dependencies
RUN pip install paho-mqtt

# Set the command to run the script
CMD ["python", "/app/vPLC_Test.py"]
