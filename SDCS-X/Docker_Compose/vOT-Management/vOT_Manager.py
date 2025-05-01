# -------------------------------------------------------------------------------------------------- #
# Project:      OT Docker Container Management Service                                               #
# Description:  Added MQTT broker communication                                                      #
# Author:       R00110936                                                                            #
# -------------------------------------------------------------------------------------------------- #

# Library Package Import Definitions
import os
import sys
import time
import csv
import uvicorn
import webbrowser
import threading
import psutil
import subprocess
import socket
import docker
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
port_no = 9970

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
INFLUXDB_URL = "http://vhis:8086"  # Use the container name in Docker network
INFLUXDB_TOKEN = "v0pWVk7e_RnmNMVce6JRRyIYiFmGLJNx5g2s3bgwELODB1O9n61URR6B_hBUkN1fhmvO6ks7zSGaprG9m0GKDA=="  # Token for authentication
INFLUXDB_ORG = "MTU"  # Organization name (set in InfluxDB UI)
INFLUXDB_BUCKET = "vHIS"  # Bucket name (created in UI)

# Initialize InfluxDB Client
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api()

# MQTT Config
BROKER = "mqtt_broker"
PORT = 1883
# Subscribe once to everything under "v#"
INITIAL_SUBSCRIBE = ("#", 0)  # Wildcard to catch anything starting with v
TAGS_FILE = os.getenv("TAGS_FILE", "/app/data/plc_tags.csv")  # Path to your CSV file

# Known services
KNOWN_SERVICES = {"vPLC", "vHMI", "vHIS", "vVIS", "vROB", "vOT-Mgmt"}

DISCOVERED = set()

# Simple users dictionary for demo
users = {
    "admin": sha256("password".encode()).hexdigest(),  # Store hashed password for security
    "user": sha256("1234".encode()).hexdigest()
}

# User login status (store in a simple dict for now, use a session or DB in production)
logged_in_users = {}

# MQTT message storage
mqtt_messages = deque(maxlen=100)

# MQTT Connection Callback
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(INITIAL_SUBSCRIBE)
    print(f"Subscribed to wildcard topic: {INITIAL_SUBSCRIBE[0]}")

# MQTT Message Callback
def on_message(client, userdata, message):
    topic = message.topic
    try:
        payload = message.payload.decode("utf-8")
    except UnicodeDecodeError:
        payload = "(unreadable payload)"

    print(f"OT Manager Service Received: '{payload}' from topic '{topic}'")
    mqtt_messages.append(f"{topic}: {payload}")

    # Auto-discover logic
    service = topic.split("/")[0]  # Get first part (e.g., vPLC)

    if service.startswith("v") and service not in DISCOVERED:
        DISCOVERED.add(service)
        print(f"Discovered new microservice: {service}")

        if service not in KNOWN_SERVICES:
            print(f"New Service '{service}' detected! Consider adding to KNOWN_SERVICES.")
    
    # Storing PLC Values to serve to /process_statistics endpoint
    tag = topic.split("/")[-1]  # Extract tag name

    if tag in tag_values:
        tag_values[tag] = payload
        print(f"Updated {tag} with value: {payload}")
    else:
        print(f"Ignoring unmatched tag: {tag}")

# Create MQTT client
try:
    mqtt_client = mqtt.Client(client_id="vOT_Manager")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(BROKER, PORT)
    mqtt_client.loop_start()

except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

# PLC Tag Loader
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
tag_values = {tag['name']: None for tag in tags}

#############################
# User Authentication Routes

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("vOT_Mgmt_Login.html", {"request": request})


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
async def get_machines(request: Request):
    username = request.cookies.get("username")
    if not username or username not in logged_in_users:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("vOT_Mgmt_Overview.html", {"request": request, "machines": machines_data})


@app.post("/add_machine")
async def add_machine(request: Request, machine_name: str = Form(...)):
    username = request.cookies.get("username")
    if not username or username not in logged_in_users:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    new_machine = {"id": f"machine_{len(machines_data) + 1}", "name": machine_name}
    machines_data.append(new_machine)
    return templates.TemplateResponse("vOT_Mgmt_Overview.html", {"request": request, "machines": machines_data})
    
    
@app.post("/remove_machine")
async def remove_machine(request: Request, machine_name: str = Form(...)):
    username = request.cookies.get("username")
    if not username or username not in logged_in_users:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    global machines_data
    machines_data = [machine for machine in machines_data if machine['name'] != machine_name]
    
    return templates.TemplateResponse("vOT_Mgmt_Overview.html", {"request": request, "machines": machines_data})


@app.get("/containers/{machine_id}")
async def container_management(request: Request, machine_id: str):
    username = request.cookies.get("username")
    if not username or username not in logged_in_users:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("index.html", {"request": request, "machine_id": machine_id})


@app.get("/machines", response_class=HTMLResponse)
async def home(request: Request):
    try:
        all_containers = docker_ctrl.list_ot_containers()
        print("All containers: ", all_containers)
        all_images = docker_ctrl.list_all_images()
        running_containers = docker_ctrl.list_running_containers()
        stopped_containers = docker_ctrl.list_stopped_containers()
    except Exception as e:
        print(f"Error retrieving containers: {e}")
        all_containers = []
        all_images = []

    return templates.TemplateResponse("vOT_Mgmt_Machines.html", {
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

def ping_host(host, count=1, timeout=1):
    try:
        output = subprocess.check_output(
            ["ping", "-c", str(count), "-W", str(timeout), host],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in output.splitlines():
            if "time=" in line:
                time_ms = float(line.split("time=")[-1].split()[0])
                return round(time_ms, 2)
    except subprocess.CalledProcessError:
        return None
    return None

def get_container_ip(container_name: str, network_name="docker_compose_OT_NETWORK"):
    try:
        container = client.containers.get(container_name)
        return container.attrs["NetworkSettings"]["Networks"][network_name]["IPAddress"]
    except Exception as e:
        print(f"[ERROR] Failed to get IP for {container_name}: {e}")
        return None


@app.get("/process_statistics")
async def get_process_statistics():
    process_data = {tag["name"]: tag_values.get(tag["name"]) for tag in tags}
    return JSONResponse(content=process_data)


@app.get("/system_status")
async def system_status():
    containers = client.containers.list(all=True)
    containers_running = sum(1 for c in containers if c.status == 'running')
    containers_stopped = sum(1 for c in containers if c.status == 'exited')
    containers_total = len(containers)
    docker_images = len(client.images.list())

    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Prepare to collect latency for ALL containers
    container_latencies = {}

    for container in containers:
        container_name = container.name
        container_ip = get_container_ip(container_name)

        if container_ip:
            latency = ping_host(container_ip)
        else:
            latency = None

        container_latencies[container_name] = latency

    system_status = {
        "containers_running": containers_running,
        "containers_stopped": containers_stopped,
        "containers_total": containers_total,
        "docker_images": docker_images,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "docker_disk_usage": disk_usage,
        "container_latencies": container_latencies
    }

    return JSONResponse(content=system_status)


@app.get("/mqtt_messages")
async def get_mqtt_messages():
    return JSONResponse(content=list(mqtt_messages))


def open_browser():
    time.sleep(2)  # Delay - ensure server has started
    
    # Open the browser automatically to the correct address
    url_app = "http://" + str(host_ip) + ":" + str(port_no)
    webbrowser.get('firefox').open(url_app)


if __name__ == "__main__":
    
    #browser_thread = threading.Thread(target=open_browser)
    #browser_thread.start()
    
    uvicorn.run(app, host=host_ip, port=port_no)
