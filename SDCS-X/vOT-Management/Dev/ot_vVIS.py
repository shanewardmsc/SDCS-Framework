import paho.mqtt.client as mqtt
import time
import random

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
DATA_TOPIC = "vVIS/result"
STATUS_TOPIC = "vVIS/status"

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="vision_service")
client.connect(BROKER, PORT)

while True:
    result = random.choice(["OK", "DEFECT"])
    state = random.choice(["RUNNING", "STOPPED"])
    print(f"Vision Sending: {result}")
    client.publish(DATA_TOPIC, result)
    client.publish(STATUS_TOPIC, state)
    time.sleep(6)
