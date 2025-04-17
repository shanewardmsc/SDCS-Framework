FROM python:3.11-slim

# Install required Python packages
RUN pip install paho-mqtt influxdb-client requests

# Add your mqtt-publisher.py script
COPY ./mqtt-publisher.py /app/mqtt-publisher.py

WORKDIR /app

# Run the publisher script
CMD ["python", "mqtt-publisher.py"]

