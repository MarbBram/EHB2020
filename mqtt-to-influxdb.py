"""
Connect to InfluxDB 2.0 - bridge from MQTT to InfluxDB
"""

from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from random import uniform
from time import sleep
import requests
import paho.mqtt.client as mqtt
import re
from typing import NamedTuple
from pprint import pprint

INFLUXDB_TOKEN = "D6ltGUKEgdSCOU9FgswD6Zp6H8faQ7MsdEE3JevpmTN-32JJSdATdyNfCOb_6SguWeAzd29NkFd6iid-mYfX9g=="
## You can generate a Token from the "Tokens Tab" in the UI
org = 'influxdata@bramderuyck.be'
# Your organization name is your e-mail address in the free version
bucket = "sensehat"
# This is the standard bucket name
OWNER = "bdr"
# Your own first name
precision = 'ms'

MQTT_ADDRESS = "hairdresser.cloudmqtt.com"
MQTT_USER = 'gkpdrpfa'
MQTT_PASSWORD = 'bvwnbQm7g5Wv'
MQTT_TOPIC = 'sense/+'  # [bme280|sense]/[temp|humid|pressure]
MQTT_REGEX = 'sense/([^/]+)'
MQTT_PORT = 'yourport'

INFLUXDB_ADDRESS = "https://eu-central-1-1.aws.cloud2.influxdata.com/"
influxdb_client = InfluxDBClient(url=INFLUXDB_ADDRESS, token=INFLUXDB_TOKEN)


class SensorData(NamedTuple):
	owner: str
	measurement: str
	value: float


def on_connect(client, userdata, flags, rc):
	""" The callback for when the client receives a CONNACK response from the server."""
	print('Connected with result code ' + str(rc))
	client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
	"""The callback for when a PUBLISH message is received from the server."""
	print(msg.topic + ' ' + str(msg.payload))
	sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
	if sensor_data is not None:
		# pprint(sensor_data)
		_send_sensor_data_to_influxdb(sensor_data)


def _parse_mqtt_message(topic, payload):
	match = re.match(MQTT_REGEX, topic)
	if match:
		measurement = match.group(1)
		owner = OWNER
		if measurement == 'status':
			return None
		return SensorData(owner, measurement, float(payload))
	else:
		return None


def _send_sensor_data_to_influxdb(sensor_data):
	json_body = [
		{
			'measurement': sensor_data.measurement,
			'tags': {
				'owner': sensor_data.owner
			},
			'fields': {
				'value': sensor_data.value
			}
		}
	]
	# json is not used
	line = "{} {}={} {}"
	timestamp = str(int(datetime.now().timestamp() * 1000))
	line = line.format(sensor_data.owner, sensor_data.measurement, sensor_data.value, timestamp)
	try:
		url = "{}api/v2/write?org={}&bucket={}&precision={}".format(INFLUXDB_ADDRESS, org, bucket, precision)
		headers = {"Authorization": "Token {}".format(INFLUXDB_TOKEN)}
		r = requests.post(url, data=line, headers=headers)
		print(line)
	except Exception as e:
		print(e)
		# this is terrible
		# any time there is a problem with the server, data will be lost
		# this is a job for Telegraf
		print("oops")
	return


def main():
	mqtt_client = mqtt.Client()
	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
	mqtt_client.on_connect = on_connect
	mqtt_client.on_message = on_message
	mqtt_client.connect(MQTT_ADDRESS, MQTT_PORT)
	mqtt_client.loop_forever()


if __name__ == '__main__':
	print('MQTT to InfluxDB bridge')
	main()
