import paho.mqtt.client as mqtt
import time
import random
from datetime import datetime

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
DATA_TOPIC = "vHIS/log"
STATUS_TOPIC = "vHIS/status"

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="historian_service")
client.connect(BROKER, PORT)

while True:
    log_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state = random.choice(["RUNNING", "STOPPED"])
    print(f"Historian Sending: {log_entry}")
    client.publish(DATA_TOPIC, log_entry)
    client.publish(STATUS_TOPIC, state)
    time.sleep(5)