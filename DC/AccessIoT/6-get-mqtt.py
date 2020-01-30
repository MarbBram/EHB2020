
MQTT_HOST = "mqtt.datacamp.com"

# Import mqtt library
import paho.mqtt.subscribe as subscribe

topic = "datacamp/iot/simple"
# Retrieve one message
msg = subscribe.simple(topic, hostname=MQTT_HOST)

# Print topic and payload
print(f"{msg.topic}, {msg.payload}")



import json
import pandas as pd
# Define function to call by callback method
def on_message(client, userdata, message):
    # Parse the message.payload
    data = json.loads(message.payload)
    store.append(data)