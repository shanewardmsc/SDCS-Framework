# -------------------------------------------------------------------------------------------------- #
# Project:      IT Docker Container Management Service                                               #
# Description:  Added MQTT broker communication                                                      #
# Author:       R00110936                                                                            #
# -------------------------------------------------------------------------------------------------- #

# Library Package Import Definitions
import os
import sys
import time
import uvicorn
import webbrowser
import threading
import paho.mqtt.client as mqtt
from docker_utils import DockerInterface, DockerController
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from collections import deque
from influxdb_client import InfluxDBClient, Point, WritePrecision
from hashlib import sha256

# Global Variables
host_ip = "0.0.0.0"
port_no = 9980

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize Docker Controller
docker = DockerInterface()
client = docker.docker_connect()
docker_ctrl = DockerController(client)

# Machine Configuration (Migrate to DB)
machines_data = [
    {"id": "00101_Depal_Cell", "name": "Robotic Depalletizer"},
    #{"id": "00102_Inspect_Cell", "name": "Vision Quality Inspection"}
]

# InfluxDB Configuration
INFLUXDB_URL = "http://localhost:8086"  # Use the container name in Docker network
INFLUXDB_TOKEN = "EfONdgGfDr3LSOgs8zdKOD12zz3sKRygX1oqibXA3lmpXCnWsA0WnOJ5bKo7S-FEHevvwf0DEEZfHqDXUbMyJg=="  # Token for authentication
INFLUXDB_ORG = "MTU"  # Organization name (set in InfluxDB UI)
INFLUXDB_BUCKET = "vHIS"  # Bucket name (created in UI)

# Initialize InfluxDB Client
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api()

# MQTT Config
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_ALL = "+/+"  # Listen to all microservices
TOPICS = {
    "vOT-Mgmt/status",
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

# Simple users dictionary for demo
users = {
    "admin": sha256("password".encode()).hexdigest(),  # Store hashed password for security
    "user": sha256("1234".encode()).hexdigest()
}

# User login status (store in a simple dict for now, use a session or DB in production)
logged_in_users = {}

# MQTT Connection Callback
MQTT_TOPIC = "vIT-Mgmt/status"
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

mqtt_messages = deque(maxlen=100)

# MQTT Message Callback
def on_message(client, userdata, message):
    topic = message.topic
    payload = ""
    try:
        payload = message.payload.decode("utf-8")
    except UnicodeDecodeError:
        False

    if topic in TOPICS:
        print(f"IT Manager Service Received: '{payload}' from topic '{topic}'")
        mqtt_messages.append(f"{topic}: {payload}")
        
        # Store MQTT messages in InfluxDB
        timestamp = int(time.time() * 1e9)  # Convert to nanoseconds
        point = Point("mqtt_messages") \
            .tag("topic", "vPLC/status") \
            .field("message", "Container started") \
            .time(timestamp, WritePrecision.NS)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

        print(f"Stored in InfluxDB: {topic} -> {payload}")
    
# Create MQTT client
try:
    mqtt_client = mqtt.Client(client_id="main_service")
    mqtt_client.on_message = on_message
    mqtt_client.connect(BROKER, PORT)
    mqtt_client.subscribe(TOPIC_ALL)  # Listen to all microservices
    mqtt_client.loop_start()
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

#############################
# User Authentication Routes

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("vIT_Mgmt_Login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Hash the password and check against stored users
    hashed_password = sha256(password.encode()).hexdigest()
    if username in users and users[username] == hashed_password:
        # Set the user as logged in (simple session tracking)
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="username", value=username)  # Store the username in the cookie
        logged_in_users[username] = True
        return response
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@app.get("/logout")
async def logout(request: Request):
    # Logout user by clearing the session (cookie)
    username = request.cookies.get("username")
    if username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("username")
        logged_in_users.pop(username, None)
        return response
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


#############################
# Protected Routes
@app.get("/")
#@app.get("/machines", response_class=HTMLResponse)
async def home(request: Request):
    try:
        all_containers = docker_ctrl.list_it_containers()
        all_images = docker_ctrl.list_all_images()
        running_containers = docker_ctrl.list_running_containers()
        stopped_containers = docker_ctrl.list_stopped_containers()
    except Exception as e:
        print(f"Error retrieving containers: {e}")
        all_containers = []
        all_images = []

    return templates.TemplateResponse("vIT_Mgmt_Machines.html", {
        "request": request,
        "all_containers": all_containers,
        "all_images": all_images,
        "running_containers": running_containers,
        "stopped_containers": stopped_containers
    })


@app.post("/start_container")
async def start_container(image: str = Form(...)):
    if not image:
        return {"error": "Image name is required"}

    image = image.strip().lower()  # Ensure lowercase and remove spaces
    mqtt_client.publish(MQTT_TOPIC, f"Starting container with image: {image}")

    try:
        container_id = docker_ctrl.run_container(image)
        mqtt_client.publish(MQTT_TOPIC, f"Container {container_id} started")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        print(f"Error starting container: {e}")
        return {"error": str(e)}


@app.post("/restart_container")
async def restart_container(container_id: str = Form(...)):
    docker_ctrl.restart_container(container_id)
    mqtt_client.publish(MQTT_TOPIC, f"Container {container_id} restarted")
    return RedirectResponse(url="/", status_code=303)


@app.post("/stop_container")
async def stop_container(container_id: str = Form(...)):
    docker_ctrl.stop_container(container_id)
    mqtt_client.publish(MQTT_TOPIC, f"Container {container_id} stopped")
    return RedirectResponse(url="/", status_code=303)


@app.post("/remove_container")
async def remove_container(container_id: str = Form(...)):
    docker_ctrl.remove_container(container_id)
    mqtt_client.publish(MQTT_TOPIC, f"Container {container_id} removed")
    return RedirectResponse(url="/", status_code=303)


@app.get("/mqtt_messages")
async def get_mqtt_messages():
    return JSONResponse(content=list(mqtt_messages))


def open_browser():
    time.sleep(2)  # Delay - ensure server has started
    
    # Open the browser automatically to the correct address
    url_app = "http://" + str(host_ip) + ":" + str(port_no)
    webbrowser.get('firefox').open(url_app)


if __name__ == "__main__":
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    
    uvicorn.run(app, host=host_ip, port=port_no)
