import paho.mqtt.client as mqtt
import time
import json
import random

BROKER = "localhost"
TOPIC = "plc/data"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker!" if rc == 0 else "Failed to connect to MQTT broker")

client.on_connect = on_connect
client.connect(BROKER, 1883, 60)

def simulate_plc():
    while True:
        payload = { "temperature": round(random.uniform(20,50), 2),"pressure": round(random.uniform(5,20),2),"timestamp": time.time(),}

        client.publish(TOPIC, json.dumps(payload))
        print(f"Payload sent: {payload}")
        time.sleep(2)


if __name__ == "__main__":
    client.loop_start()
    simulate_plc()
