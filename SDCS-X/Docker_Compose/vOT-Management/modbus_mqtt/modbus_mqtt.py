import os
import time
import socket
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException, ConnectionException
import paho.mqtt.client as mqtt

# --- Configuration ---
PLC_HOST = "vplc"
PLC_PORT = 502
PLC_ID = "main"
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt_broker")
MQTT_PORT = 1883
MQTT_BASE_TOPIC = f"sdcs/vplc/{PLC_ID}/tag"

READ_INTERVAL = 1  # seconds
MODBUS_REGISTER_RANGE = range(0, 1)  # Just reading MW0

# --- Wait Functions ---
def wait_for_service(name, host, port, timeout=30):
    print(f"[INIT] Waiting for {name} at {host}:{port} (timeout: {timeout}s)...")
    start = time.time()
    while True:
        try:
            socket.create_connection((host, port), timeout=2)
            print(f"[OK] {name} is reachable at {host}:{port}.")
            return
        except OSError as e:
            if time.time() - start > timeout:
                print(f"[ERROR] Timed out waiting for {name} after {timeout}s.")
                raise TimeoutError(f"Could not reach {name} at {host}:{port} after {timeout}s")
            print(f"[WAITING] {name} not reachable yet ({e}). Retrying...")
            time.sleep(2)

wait_for_service("MQTT broker", MQTT_BROKER, MQTT_PORT)
wait_for_service("PLC", PLC_HOST, PLC_PORT)

# --- MQTT Setup ---
print("[MQTT] Initializing MQTT client...")
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="main_service")

print(f"[MQTT] Connecting to broker at {MQTT_BROKER}:{MQTT_PORT}...")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()
print("[MQTT] Client loop started.")

# --- Modbus Client ---
def get_modbus_client():
    print("[Modbus] Attempting to connect to OpenPLC...")
    client = ModbusTcpClient(PLC_HOST, port=PLC_PORT, timeout=3)
    if client.connect():
        print("[Modbus] Connected to OpenPLC Modbus server.")
        return client
    else:
        print("[Modbus] Failed to connect to OpenPLC Modbus server.")
        client.close()
        return None

modbus_client = get_modbus_client()

# --- Main Polling Loop ---
print("[MAIN] Entering main polling loop.")
try:
    while True:
        if not modbus_client:
            print("[MAIN] Reconnecting to Modbus server in 3s...")
            time.sleep(3)
            modbus_client = get_modbus_client()
            continue

        for address in MODBUS_REGISTER_RANGE:
            try:
                print(f"[READ] Reading Modbus address {address}...")
                start_time = time.time()

                response = modbus_client.read_holding_registers(address=address, count=1, slave=1)

                if response is None:
                    print(f"[Modbus Warning] Null response from address {address}")
                    continue
                if not hasattr(response, 'registers'):
                    print(f"[Modbus Warning] Invalid response structure at address {address}")
                    continue

                value = response.registers[0]
                topic = f"{MQTT_BASE_TOPIC}/{address}"
                payload = str(value)

                print(f"[MQTT] Publishing: {topic} → {payload}")
                mqtt_client.publish(topic, payload)

                latency = (time.time() - start_time) * 1000
                print(f"[SUCCESS] Published with latency: {latency:.2f} ms")

            except (ModbusException, ConnectionException, OSError) as e:
                print(f"[Modbus Error] Exception occurred while reading address {address}: {e}")
                print("[Modbus] Closing connection and retrying in 3s...")
                try:
                    modbus_client.close()
                except:
                    pass
                del modbus_client
                modbus_client = None
                time.sleep(3)
                break  # break from the loop to reconnect

        print(f"[WAIT] Sleeping for {READ_INTERVAL}s...\n")
        time.sleep(READ_INTERVAL)

except KeyboardInterrupt:
    print("[EXIT] Caught keyboard interrupt. Stopping service...")

finally:
    if modbus_client:
        print("[CLEANUP] Closing Modbus client connection.")
        try:
            modbus_client.close()
        except:
            pass
    print("[CLEANUP] Stopping MQTT loop and disconnecting.")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("[CLEANUP] Shutdown complete.")

