FROM python:3.11-slim

# Install necessary logging dependencies
RUN pip install loguru requests

# Copy the log collection script
COPY log_collector.py /app/log_collector.py

# Set the working directory
WORKDIR /app

# Run the log collection script
CMD ["python", "log_collector.py"]
