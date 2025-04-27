FROM docker.io/shanewardmsc/sdcs-x-influxdb:v1.5

# Install Python + dependencies
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 install paho-mqtt influxdb-client

# Set working dir
WORKDIR /app

# Copy scripts
COPY mqtt_to_influx.py /app/
COPY plc_tags.csv /app/
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Use our custom startup script
ENTRYPOINT ["/start.sh"]

