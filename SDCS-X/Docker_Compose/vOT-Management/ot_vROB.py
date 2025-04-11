import paho.mqtt.client as mqtt
import time
import random

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
DATA_TOPIC = "vROB/task"
STATUS_TOPIC = "vROB/status"

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="robot_service")
client.connect(BROKER, PORT)

while True:
    task = random.choice(["PICKING", "PLACING"])
    state = random.choice(["RUNNING", "STOPPED"])
    print(f"Robot Sending: {task}")
    client.publish(DATA_TOPIC, task)
    client.publish(STATUS_TOPIC, state)
    time.sleep(3)
