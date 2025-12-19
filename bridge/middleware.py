import json
import math
import logging
import requests
import paho.mqtt.client as mqtt

# --- Configuration ---
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "loopservices/{mathias}/sensors/raw"
API_URL = "http://127.0.0.1:8000/api/readings"

# 
# --- Logging --- 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger("IoT-Middleware")

# --- TODO: Implement your logic below ---

def try_parse_float(value):

    # Early escape if variable type is nothing
    if value is None: return None 
    
    # Try and parse into a float value
    try: 
        value = float(value) 
    except (TypeError, ValueError): 
        # If failed, early exit 
        return None 
    
    # Reject NaN and +/-inf 
    if not math.isfinite(value):
        return None 
    
    return value

# Validates and normalizes a raw MQTT JSON payload.
# If valid, POSTs the reading to the backend API.
def sanitize_and_send(payload):
    """
    Task 1: The Middleware
    1.1: Parse the JSON payload.
    1.2: Normalize keys ('t' -> 'temperature', 'h' -> 'humidity').
    1.3: Validate data (filter out impossible values).
    1.4: Send valid data to API_URL via POST request.
    """

    # 1.1: Parse the JSON payload 
    # Formatting the `str` input into a JSON format 
    try: 
        raw_data = json.loads(payload)
    except json.JSONDecodeError:
        logger.info("REJECT: invalid JSON payload") 
        return None 
    
    # 1.2: Transforming the variables `t` and `h` into ReadingSchema format
    # ReadingSchema is defined in backend/main.py lines 32 - 34 
    temperature_value = raw_data.get("t")
    humidity_value = raw_data.get("h")

    # 1.3.1: Calling `try_parse_float(value)` 
    temperature_value = try_parse_float(temperature_value)
    humidity_value = try_parse_float(humidity_value)
    
    if temperature_value is None or humidity_value is None: 
        logger.info("REJECT: non-numeric values (t=%r, h=%r)", raw_data.get("t"), raw_data.get("h"))
        return None 

    # 1.3.2: Validate ranges 
    if not (-50.0 <= temperature_value <= 100.0): 
        logger.info("REJECT: temperature out of range (t=%s)", temperature_value)
        return None 
    if not (0.0 <= humidity_value <= 100.0):
        logger.info("REJECT: humidity out of range (h=%s)", humidity_value)
        return None 
    
    normalized = {
        "temperature": temperature_value,
        "humidity": humidity_value
    }

    # 1.4: Post to Backend 
    # https://requests.readthedocs.io/en/latest/user/quickstart/ 
    try:
        backend_response = requests.post(API_URL, json=normalized, timeout=5)
    except requests.RequestException as e:
        logger.warning("REJECT: post failed (%s)", e)
        return None

    if 200 <= backend_response.status_code < 300:
        logger.info("ACCEPT: backend accepted (%s) %s", backend_response.status_code, normalized)
        return True
    else:
        logger.warning("DROP: backend rejected (%s): %s", backend_response.status_code)
        return None    

# --- MQTT Setup ---

# On success, subscribes to the configured topic 
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}")
    else:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)

# Decodes the payload and forwards it to the sanitizer/HTTP sender 
def on_message(client, userdata, msg):
    # `msg.payload.decode()` transforms the message into a str format
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