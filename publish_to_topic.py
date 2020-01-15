import paho.mqtt.client as mqtt
import time, datetime
from random import uniform, choice


# from sense_hat import SenseHat
# sense = SenseHat()
# set up mqtt client
client = mqtt.Client("python_pub")
# set mqtt username/pw
client.username_pw_set(username="gkpdrpfa", password="bvwnbQm7g5Wv")
# set server to publish to
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
		#client.publish("sense/humid", humid)
		client.publish("sense/humid", uniform(3.0, 99.9))

		# pressure = sense.get_pressure()
		# temp = sense.get_temperature()
		# humid = sense.get_humidity()
		pressure = 930.4

		client.publish("sense/pressure", pressure)
		green = "#4feb34"
		red = "#eb4034"
		orange = "#eb9334"
		color = choice([green, red, orange])
		client.publish("sense/color", color )
		#pause for 10 seconds
		client.publish("second", datetime.datetime.now().second )
		time.sleep(.5)

	# deal nicely with ^C
except KeyboardInterrupt:
	print("interrupted!")
client.loop_stop()

