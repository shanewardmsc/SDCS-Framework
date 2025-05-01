import os
import time
import csv
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- Configurations ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt_broker")
MQTT_PORT = 1883
INFLUX_URL = os.getenv("INFLUX_URL", "http://0.0.0.0:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "MTU")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "vHIS")
TAGS_FILE = os.getenv("TAGS_FILE", "/app/plc_tags.csv")

print("Influx Client DB")
# --- InfluxDB Client ---
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

print("Loading CSV Tag Function")
# --- Load Tags from CSV ---
def load_tags_from_csv():
    tags = []
    with open(TAGS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tags.append({
                'name': row['tag_name'],
                'address': int(row['modbus_address']),
                'type': row['data_type'].upper(),
                'function': row['modbus_function'].lower()
            })
    return tags

print("Load CSV Tags")
# Load tags at startup
tags = load_tags_from_csv()

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[MQTT] Connected with result code {rc}")
    
    # Check if connection was successful
    if rc != 0:
        print(f"[MQTT] Failed to connect to the broker. Result code: {rc}")
        return
    
    # Subscribe to topics based on loaded tags
    for tag in tags:
        topic = f"vHIS/tag/{tag['name']}"
        client.subscribe(topic)
        print(f"[MQTT] Subscribed to: {topic}")

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected from broker. Result code: {rc}")

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    
    # Ensure the topic has the correct structure
    if len(topic_parts) < 3:
        print(f"[WARNING] Invalid topic structure: {msg.topic}")
        return

    # Extract tag name based on the assumption the last part is the tag name
    tag_name = topic_parts[-1]

    # Find the tag in the loaded tags list
    tag = next((t for t in tags if t['name'] == tag_name), None)
    if not tag:
        print(f"[WARNING] Tag not found: {tag_name}")
        return

    try:
        # Decode the payload and always convert to float
        value = float(msg.payload.decode())

        point = Point("plc_tag") \
            .tag("tag_name", tag_name) \
            .tag("address", str(tag['address'])) \
            .field("value", value) \
            .time(datetime.utcnow().isoformat() + "Z")

        write_api.write(bucket=INFLUX_BUCKET, record=point)
        print(f"[INFLUX] Wrote: {tag_name} → {value}")

    except ValueError as e:
        print(f"[ERROR] Could not convert payload to float: {e}")
    except Exception as e:
        print(f"[INFLUX ERROR] Failed to write point: {e}")

# --- MQTT Client Setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt_to_influx")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print(f"[MQTT] Connecting to broker at {MQTT_BROKER}:{MQTT_PORT}...")
try:
    # Connect to the broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Add a debugging loop to listen for all topics (optional)
    print(f"[MQTT] Subscribed to all topics.")
    client.subscribe("#")  # Subscribe to all topics to monitor incoming messages

    # Start the loop
    client.loop_start()

    # Main loop to print messages
    while True:
        time.sleep(5)  # Allow time for messages to come in and get logged
except Exception as e:
    print(f"[ERROR] Failed to connect to broker: {e}")
finally:
    client.loop_stop()
    print("[EXIT] Stopped MQTT client loop.")

