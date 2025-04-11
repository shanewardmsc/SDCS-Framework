import paho.mqtt.client as mqtt
import time
import random

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
DATA_TOPIC = "vHMI/alarm"
STATUS_TOPIC = "vHMI/status"

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="hmi_service")
client.connect(BROKER, PORT)

while True:
    alarm_status = random.choice(["ALARM_ACTIVE", "NO_ALARM"])
    state = random.choice(["RUNNING", "STOPPED"])
    print(f"HMI Sending: {alarm_status}")
    client.publish(DATA_TOPIC, alarm_status)
    client.publish(STATUS_TOPIC, state)
    time.sleep(4)