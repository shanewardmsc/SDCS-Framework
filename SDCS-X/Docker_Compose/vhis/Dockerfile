FROM docker.io/shanewardmsc/sdcs-x-influxdb:v1.5

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-venv && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY mqtt_to_influx.py plc_tags.csv ./

RUN python3 -m venv venv
RUN ./venv/bin/pip install --no-cache-dir paho-mqtt influxdb-client

EXPOSE 8086

# ENTRYPOINT replicating start.sh logic
CMD bash -c "\
    echo '[STARTUP] Starting InfluxDB...' && \
    influxd & \
    echo '[STARTUP] Waiting for InfluxDB...' && \
    until influx bucket list --org \"${INFLUX_ORG}\" --token \"${INFLUX_TOKEN}\" >/dev/null 2>&1; do \
      echo '[STARTUP] InfluxDB not ready, waiting 5 seconds...'; \
      sleep 5; \
    done && \
    echo '[STARTUP] InfluxDB ready!' && \
    echo '[STARTUP] Starting mqtt_to_influx.py...' && \
    ./venv/bin/python -u /app/mqtt_to_influx.py"

