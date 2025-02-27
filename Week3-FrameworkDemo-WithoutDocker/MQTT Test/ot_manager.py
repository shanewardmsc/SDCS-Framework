import paho.mqtt.client as mqtt

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_ALL = "+/+"  # Listen to all microservices
TOPICS = {
    "vPLC/state",
    "vPLC/status",
    "vHMI/alarm",
    "vHMI/status",
    "vHIS/log",
    "vHIS/status",
    "vVIS/result",
    "vVIS/status",
    "vROB/task",
    "vROB/status"
}
DISCOVERED = set()

# Callback when receiving messages
def on_message(client, userdata, message):
    topic = message.topic
    try:
        payload = message.payload.decode("utf-8")
        #print(f"Main Service Received: '{payload}' from topic '{topic}'")
    except UnicodeDecodeError:
        False
        #print(f"Received non-UTF-8 message from topic '{topic}': {message.payload}")

    # Service Discovery - Log new topics dynamically
    if topic not in DISCOVERED:
        DISCOVERED.add(topic)
        #print(f"Discovered new topic: {topic}")

    # Only process messages from known microservices
    if topic in TOPICS:
        print(f"OT Manager Service Received: '{payload}' from topic '{topic}'")

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="main_service")
client.on_message = on_message

# Connect and subscribe to wildcard topic
client.connect(BROKER, PORT)
client.subscribe(TOPIC_ALL)  # Listen to all microservices

# Start listening
client.loop_forever()
