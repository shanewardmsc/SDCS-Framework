#!/bin/sh

# Add default route via the router
ip route add 192.168.3.0/24 via 192.168.2.254

# Start OpenPLC in the background
./start_openplc.sh &

# Wait a bit for OpenPLC to be ready (or use a better check)
sleep 5

# Start Modbus-to-MQTT script
python3 /app/modbus_mqtt.py

