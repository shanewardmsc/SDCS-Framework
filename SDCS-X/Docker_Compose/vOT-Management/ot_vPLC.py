import paho.mqtt.client as mqtt
import time
import random

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
DATA_TOPIC = "vPLC/state"
STATUS_TOPIC = "vPLC/status"

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="plc_service")
client.connect(BROKER, PORT)

while True:
    state = random.choice(["RUNNING", "STOPPED"])
    print(f"PLC Sending: {state}")
    client.publish(DATA_TOPIC, state)
    client.publish(STATUS_TOPIC, state)
    time.sleep(3)