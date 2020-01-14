import paho.mqtt.client as mqtt
import time
from random import uniform

# from sense_hat import SenseHat
# sense = SenseHat()
# set up mqtt client
client = mqtt.Client("python_pub")
#set mqtt username/pw
client.username_pw_set(username="gkpdrpfa", password="bvwnbQm7g5Wv")
#set server to publish to
client.connect("hairdresser.cloudmqtt.com", 18875)
client.loop_start()
# What is this?
# http://www.steves-internet-guide.com/loop-python-mqtt-client/

try:
	while True:
		#publish temp to topic
		#client.publish("sense/temp", sense.get_temperature())
		client.publish("sense/temp", uniform(3.0, 27.0))
		#publish humidity
		#client.publish("sense/humid", sense.get_humidity())
		client.publish("sense/humid", uniform(3.0, 99.9))
		#pause for 10 seconds
		time.sleep(2)
	#deal nicely with ^C
except KeyboardInterrupt:
	print("interrupted!")
client.loop_stop()