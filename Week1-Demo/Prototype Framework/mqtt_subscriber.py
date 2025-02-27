import grpc
import analytics_pb2
import analytics_pb2_grpc
import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
TOPIC = "plc/data"

# Connect to IT microservice via gRPC
channel = grpc.insecure_channel("localhost:50051")
grpc_client = analytics_pb2_grpc.AnalyticsServiceStub(channel)

# MQTT callback
def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    print(f"Received MQTT data: {payload}")

    # send data to it microservice via gRPC
    response = grpc_client.Compute(analytics_pb2.AnalyticsRequest(data=[payload["temperature"], payload["pressure"]]))
    print(f"Analytics -> Mean: {response.mean}, Max: {response.max}, Min: {response.min}, Sum: {response.sum}")

mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, 1883, 60)
mqtt_client.subscribe(TOPIC)
mqtt_client.on_message = on_message
mqtt_client.loop_forever()

