import os
import time
import requests
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB setup
url = os.getenv("INFLUX_URL", "http://influxdb:8086")
token = os.getenv("INFLUX_TOKEN", "my-token")
org = os.getenv("INFLUX_ORG", "sdcs-x-org")
bucket = os.getenv("INFLUX_BUCKET", "sdcs-x-bucket")

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# MQTT setup
mqtt_broker = "mqtt-broker"  # Replace with your MQTT broker address (if needed)
mqtt_port = 1883
mqtt_topic = "openplc/tags"

mqtt_client = mqtt.Client()

connected = False
while not connected:
    try:
        mqtt_client.connect(mqtt_broker, mqtt_port, 60)
        connected = True
    except Exception as e:
        print(f"MQTT connection failed: {e}, retrying in 3s...")
        time.sleep(3)

# OpenPLC API endpoint
openplc_url = "http://openplc:8080/api/v1/vars"

# Function to fetch tags from OpenPLC API
def get_openplc_tags():
    try:
        response = requests.get(openplc_url)
        if response.status_code == 200:
            return response.json()  # Returns a list of tags in JSON format
        else:
            print(f"Error: Unable to fetch tags (status {response.status_code})")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Publish tags to InfluxDB
def publish_tags_to_influxdb(tags):
    timestamp = time.time_ns()
    for tag in tags:
        tag_name = tag.get("name")
        tag_value = tag.get("value")
        if tag_name and tag_value is not None:
            point = Point("plc_tags").tag("name", tag_name).field("value", tag_value).time(timestamp)
            write_api.write(bucket=bucket, org=org, record=point)
            print(f"Published to InfluxDB: {tag_name}={tag_value}")

# Publish tags to MQTT
def publish_tags_to_mqtt(tags):
    for tag in tags:
        tag_name = tag.get("name")
        tag_value = tag.get("value")
        if tag_name and tag_value is not None:
            mqtt_message = f"{tag_name}={tag_value}"
            mqtt_client.publish(mqtt_topic, mqtt_message)
            print(f"Published to MQTT: {tag_name}={tag_value}")

# Main loop
while True:
    tags = get_openplc_tags()
    if tags:
        publish_tags_to_influxdb(tags)
        publish_tags_to_mqtt(tags)
    time.sleep(2)  # Sleep for 2 seconds before fetching again

