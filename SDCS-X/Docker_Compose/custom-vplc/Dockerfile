# Start from the OpenPLC image
FROM docker.io/shanewardmsc/sdcs-x-openplc:v1.4

# Set working directory
WORKDIR /app

# Copy your modbus_mqtt.py script and requirements.txt into the container
COPY modbus_mqtt.py /app/modbus_mqtt.py
COPY requirements.txt /app/requirements.txt

# Install Python, pip, and other dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv netcat-openbsd && \
    python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Set environment to use the virtualenv
ENV PATH="/app/venv/bin:$PATH"

# Expose the necessary ports for OpenPLC and the MQTT broker
EXPOSE 50
EXPOSE 8080
EXPOSE 1883

# Wait for OpenPLC to be ready and then start the script
CMD bash -c "while ! nc -z localhost 502; do echo 'Waiting for OpenPLC...'; sleep 2; done; python /app/modbus_mqtt.py"

