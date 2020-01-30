import paho.mqtt.client as mqtt
import time, datetime

from random import uniform, choice, random
import requests
from pprint import  pprint
from random import randint


# from sense_hat import SenseHat
# sense = SenseHat()
# set up mqtt client
client = mqtt.Client("python_pub")
# set mqtt username/pw

# set server to publish to
client.connect("test.mosquitto.org", 1883)
client.loop_start()
# What is this?
# http://www.steves-internet-guide.com/loop-python-mqtt-client/



def publish_mqtt(prevous_number):
	try:
		now = datetime.datetime.now().strftime("%H:%M:%S")
		inhoud = '{"timestamp": 1579211282, "humidity": 60, "temperature": 21}'
		inhoudB = '{"timestamp": 1579211282, "category": "humidity", "value": 21.3}'
		client.publish("iot/simple", inhoud)
		client.publish("datacamp/iot/simple", inhoud)
		client.publish("EHB2020/iot/simple", "Good luck with your examen. Time is: "+now)
		client.publish("ehb2020/iot/simple", "Good luck with your examen. Time is: " + now)
		new_number = prevous_number + randint(0,30)
		client.publish("datacamp/energy", new_number)
		client.publish("paho/test/iot_course", inhoudB)

	except Exception as e:
		print(e)
	return new_number


try:
	num = 6000
	while True:
		num = publish_mqtt(num)
		time.sleep(5.4)

except KeyboardInterrupt:
	# deal nicely with ^C
	print("interrupted!")

client.loop_stop()

