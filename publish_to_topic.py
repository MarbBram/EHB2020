import paho.mqtt.client as mqtt
import time, datetime
from random import uniform, choice, random
import requests
from pprint import  pprint


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

def outside_temp():
	settings = {
		'api_key': '147222e24d94d28440b5c61b9dd630f0',
		'zip_code': '9770',
		'country_code': 'be',
		'temp_unit': 'metric'}  # unit can be metric, imperial, or kelvin
	BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"
	final_url = BASE_URL.format(settings["api_key"], settings["zip_code"], settings["country_code"],
								settings["temp_unit"])
	weather_data = requests.get(final_url).json()
	# pprint(weather_data)
	outside_tem = weather_data["main"]["temp"]
	return outside_tem

def publish_mqtt():
	try:

		"""
			Get sensor data
		"""
		# pressure = sense.get_pressure()
		pressure = uniform(940.0, 990.9)
		pressure = round(pressure, 2)

		temp = uniform(3.0, 27.0)
		# temp = sense.get_temperature()
		temp = round(temp, 1)
		# humid = sense.get_humidity()
		humid = uniform(80.0, 99)
		humid = round(humid, 3)
		"""
			Publish to MQTT
		"""
		client.publish("sense/temp", temp)
		client.publish("sense/pressure", pressure)
		client.publish("sense/humid", humid)

		"""
			Color coding temperature
		"""
		green = "#4feb34"
		red = "#eb4034"
		orange = "#eb9334"
		color = choice([green, red, orange])
		client.publish("sense/color", color)
		# pause for 10 seconds
		client.publish("second", datetime.datetime.now().second)

	except Exception as e:
		print(e)
	return


try:
	while True:
		publish_mqtt()
		time.sleep(2.4)
		if random() < 0.01:
			x = outside_temp()
			client.publish("sense/outsidetemp", round(x, 1))

except KeyboardInterrupt:
	# deal nicely with ^C
	print("interrupted!")

client.loop_stop()

