import json
import requests
import paho.mqtt.client as mqtt

# --- Configuration ---
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "loopservices/{mathias}/sensors/raw"
API_URL = "http://127.0.0.1:8000/api/readings"

# --- TODO: Implement your logic below ---

# Validates and normalizes a raw MQTT JSON payload.
# If valid, POSTs the reading to the backend API.
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

# On success, subscribes to the configured topic.
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}")
    else:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)

# Decodes the payload and forwards it to the sanitizer/HTTP sender.
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    sanitize_and_send(payload)

if __name__ == "__main__":

    # Creating an MQTT client object, which will manage the connection and message handling 
    # https://incore.readthedocs.io/en/latest/InCore.Mqtt/MqttClient.html
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assigning the 'on_connect' and 'on_message' functions to the MQTT client object 
    client.on_connect = on_connect
    client.on_message = on_message

    print("Middleware starting...")
    client.connect(MQTT_BROKER, 1883, 60)
    
    # Blocking loop to process network traffic
    client.loop_forever()
