#!/bin/bash

# Start InfluxDB in the background
influxd &

# Wait a bit to make sure influxd is running (optional tuning)
sleep 5

# Start the MQTT-to-Influx bridge
echo "[START] Running mqtt_to_influx.py..."
python3 /app/mqtt_to_influx.py
