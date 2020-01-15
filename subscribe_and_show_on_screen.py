import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected to MQTT broker with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("second")
	return


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print("got message on topic %s : %s" % (msg.topic, msg.payload))
	# sense.show_message("MQTT Temp = %.2f" % (float(msg.payload)))
	print("MQTT Temp = %.2f" % (float(msg.payload)))
	return


### MAIN ###
client = mqtt.Client()
MQTT_ADDRESS = "hairdresser.cloudmqtt.com"
MQTT_USER = 'gkpdrpfa'
MQTT_PASSWORD = 'bvwnbQm7g5Wv'
client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_ADDRESS, 18875)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:
	client.loop_forever()
# deal nicely with ^C
except KeyboardInterrupt:
	print("interrupted!")