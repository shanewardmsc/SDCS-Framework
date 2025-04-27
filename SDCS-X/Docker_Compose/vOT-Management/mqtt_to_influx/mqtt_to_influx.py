import os
import time
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- Configurations ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt_broker")
MQTT_PORT = 1883
MQTT_TOPIC = "sdcs/vplc/+/tag/+"

INFLUX_URL = os.getenv("INFLUX_URL", "http://vhis:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "v0pWVk7e_RnmNMVce6JRRyIYiFmGLJNx5g2s3bgwELODB1O9n61URR6B_hBUkN1fhmvO6ks7zSGaprG9m0GKDA==")
INFLUX_ORG = os.getenv("INFLUX_ORG", "MTU")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "vHIS")

# --- InfluxDB Client ---
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"[MQTT] Subscribed to: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    if len(topic_parts) != 5:
        print(f"[WARNING] Invalid topic structure: {msg.topic}")
        return

    _, _, plc_id, _, tag_address = topic_parts
    try:
        value = float(msg.payload.decode())
        point = Point("plc_tag") \
            .tag("plc", plc_id) \
            .tag("address", tag_address) \
            .field("value", value) \
            .time(time.time_ns())

        write_api.write(bucket=INFLUX_BUCKET, record=point)
        print(f"[INFLUX] Wrote: {plc_id}:{tag_address} → {value}")

    except ValueError as e:
        print(f"[ERROR] Could not convert payload to float: {e}")
    except Exception as e:
        print(f"[INFLUX ERROR] Failed to write point: {e}")

# --- MQTT Client Setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt_to_influx")
client.on_connect = on_connect
client.on_message = on_message

print(f"[MQTT] Connecting to broker at {MQTT_BROKER}:{MQTT_PORT}...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
