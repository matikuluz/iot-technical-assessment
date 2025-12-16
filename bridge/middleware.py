import json
import requests
import paho.mqtt.client as mqtt

# --- Configuration ---
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "loopservices/{your_first_name}/sensors/raw"
API_URL = "http://127.0.0.1:8000/api/readings"

# --- TODO: Implement your logic below ---

def sanitize_and_send(payload):
    """
    1. Parse the JSON payload.
    2. Normalize keys ('t' -> 'temperature', 'h' -> 'humidity').
    3. Validate data (filter out impossible values).
    4. Send valid data to API_URL via POST request.
    """
    print(f"Received raw: {payload}")
    # Write your code here...

# --- MQTT Setup ---

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}")
    else:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    sanitize_and_send(payload)

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    print("Middleware starting...")
    client.connect(MQTT_BROKER, 1883, 60)
    
    # Blocking loop to process network traffic
    client.loop_forever()