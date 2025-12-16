import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org" # Public test broker
TOPIC = "loopservices/{your_first_name}/sensors/raw"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print(f"Device started. Publishing to {TOPIC}...")

while True:
    if random.random() > 0.1:
        payload = {
            "t": round(random.uniform(20.0, 30.0), 2),
            "h": round(random.uniform(40.0, 60.0), 2)
        }
    else:
        payload = {
            "t": random.choice([200.0, None, "error"]), 
            "h": -50.0 
        }

    client.publish(TOPIC, json.dumps(payload))
    print(f"Published: {payload}")
    time.sleep(2)