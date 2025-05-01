#!/bin/bash

#!/bin/bash

# Start InfluxDB in the background
echo "[STARTUP] Starting InfluxDB..."
influxd &

# Wait for InfluxDB to be fully initialized
echo "[STARTUP] Waiting for InfluxDB..."
until influx bucket list --org "$INFLUX_ORG" --token "$INFLUX_TOKEN" >/dev/null 2>&1; do
  echo "[STARTUP] InfluxDB not ready, waiting 5 seconds..."
  sleep 5
done

# Check if Influx is already initialized
if ! influx bucket list --org "$INFLUX_ORG" --token "$INFLUX_TOKEN" >/dev/null 2>&1; then
  echo "[INIT] InfluxDB not initialized, running setup..."
  influx setup \
    --username "$DOCKER_INFLUXDB_INIT_USERNAME" \
    --password "$DOCKER_INFLUXDB_INIT_PASSWORD" \
    --org "$INFLUX_ORG" \
    --bucket "$INFLUX_BUCKET" \
    --token "$INFLUX_TOKEN" \
    --force
else
  echo "[INIT] InfluxDB already initialized."
fi

# Run the Python MQTT bridge
echo "[STARTUP] Starting mqtt_to_influx.py..."
/app/venv/bin/python /app/mqtt_to_influx.py
echo "[STARTUP] mqtt_to_influx.py started."

