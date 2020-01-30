# Import mqtt library
import paho.mqtt.subscribe as subscribe

MQTT_HOST = "mqtt.datacamp.com"

cache = []


def on_message(client, userdata, message):
	# Combine timestamp and payload
	data = f"{message.timestamp},{message.payload}"
	# Append data to cache
	cache.append(data)


# Connect function to mqtt datastream
subscribe.callback(on_message, topics="datacamp/energy", hostname=MQTT_HOST)


# Convert the timestamp
df["ts"] = pd.to_datetime(df["ts"])

# Print datatypes and first observations
print(df.dtypes)
print(df.head())
