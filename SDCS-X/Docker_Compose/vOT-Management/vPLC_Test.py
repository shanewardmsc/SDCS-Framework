# mqtt_client.py
import paho.mqtt.client as mqtt
import time
import random

# MQTT Configuration
BROKER = "test.mosquitto.org"
PORT = 1883
DATA_TOPIC = "vPLC/state"
STATUS_TOPIC = "vPLC/status"
TOPIC_ALL = "+/+"  # Listen to all microservices

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(TOPIC_ALL)  # Subscribe to all topics

    # Publish a message after connecting
    publish_message(client)

# Callback for when a message is received
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    print(f"Received message: '{payload}' from topic '{topic}'")

# Function to publish a message to the broker
def publish_message(client):

    state = random.choice(["RUNNING", "STOPPED"])
    print(f"PLC Sending: {state}")
    client.publish(DATA_TOPIC, state)
    client.publish(STATUS_TOPIC, state)

# Create an MQTT client and set callbacks
client = mqtt.Client(client_id="vPLC_Test")
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect to the broker and start listening for messages
    client.connect(BROKER, PORT)
    client.loop_start()  # Start the loop to process callbacks

    # Wait some time before publishing more messages (for example, every 5 seconds)
    while True:
        time.sleep(2)
        publish_message(client)

except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
