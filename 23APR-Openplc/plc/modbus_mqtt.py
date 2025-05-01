import os
import time
import socket
import struct
import csv
import paho.mqtt.client as mqtt
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException, ConnectionException

# --- Configuration ---
PLC_HOST = "0.0.0.0"
PLC_PORT = 502
PLC_ID = "Main PLC"
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt_broker")
MQTT_PORT = 1883
MQTT_BASE_TOPIC = f"vPLC/{PLC_ID}/"
READ_INTERVAL = 1  # seconds

# --- Wait Functions ---
def wait_for_service(name, host, port, timeout=60):
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
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="vPLC")

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

# --- Load Tags from CSV ---
def load_tags_from_csv():
    tags = []
    with open("/app/data/plc_tags.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tags.append({
                'name': row['tag_name'],
                'address': int(row['modbus_address']),
                'type': row['data_type'].upper(),  # "INT", "REAL", or "BOOL"
                'function': row['modbus_function'].lower()  # "holding_register" or "coil"
            })
    return tags


tags = load_tags_from_csv()  # or load from a DB if desired

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

        for tag in tags:
            tag_name = tag['name']
            address = tag['address']
            data_type = tag['type']
            function = tag['function']
            try:
                print(f"[READ] {tag_name} ({function.upper()}, {data_type}) at address {address}...")
                start_time = time.time()

                if function == 'holding_register':
                    if data_type == 'INT':
                        # Read a 16-bit INT (1 register)
                        response = modbus_client.read_holding_registers(address=address, count=1, slave=1)
                        if response and hasattr(response, 'registers'):
                            value = response.registers[0]
                            print(f"[SUCCESS] {tag_name} (INT) value: {value}")

                    
                    elif data_type == 'REAL':
                        # Read a 32-bit REAL (2 registers)
                        response = modbus_client.read_holding_registers(address=address, count=2, slave=1)
                        if response and hasattr(response, 'registers') and len(response.registers) == 2:
                            # Combine registers into a 4-byte array
                            byte_data = bytearray()
                            byte_data.extend(response.registers[0].to_bytes(2, byteorder='big'))
                            byte_data.extend(response.registers[1].to_bytes(2, byteorder='big'))

                            # Attempt unpacking in both byte orders for diagnostic
                            try:
                                value = struct.unpack('>f', byte_data)[0]
                                value = f"{value:.5f}"
                                print(f"[SUCCESS] {tag_name} (REAL) value (Big-Endian): {value}")
                            except Exception as e:
                                print(f"[ERROR] Big-Endian unpacking failed for {tag_name}: {e}")

                        else:
                            print(f"[ERROR] Unexpected register count for {tag_name} (REAL).")
                    else:
                        print(f"[WARN] Unsupported data type: {data_type} for tag {tag_name}")
                        continue

                elif function == 'coil':
                    response = modbus_client.read_coils(address=address, count=1, slave=1)
                    if response and hasattr(response, 'bits'):
                        value = int(response.bits[0])
                        print(f"[SUCCESS] {tag_name} (COIL) value: {value}")
                    else:
                        print(f"[ERROR] Failed to read coil at address {address} for tag {tag_name}.")
                else:
                    print(f"[WARN] Unsupported function: {function} for tag {tag_name}")
                    continue

                topic = f"{MQTT_BASE_TOPIC}/{tag_name}"
                mqtt_client.publish(topic, str(value))
                print(f"[MQTT] Publishing: {topic} → {str(value)}")


                latency = (time.time() - start_time) * 1000
                print(f"[SUCCESS] Published with latency: {latency:.2f} ms\n")

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
        except Exception:
            pass
    print("[CLEANUP] Stopping MQTT loop and disconnecting.")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("[CLEANUP] Shutdown complete.")
