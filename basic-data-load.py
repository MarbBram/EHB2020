"""
Connect to InfluxDB 2.0 - write data and query them
"""

from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from random import uniform
from time import sleep
import requests
# from sense_hat import SenseHat
# sense = SenseHat()


my_token = "D6ltGUKEgdSCOU9FgswD6Zp6H8faQ7MsdEE3JevpmTN-32JJSdATdyNfCOb_6SguWeAzd29NkFd6iid-mYfX9g=="
## You can generate a Token from the "Tokens Tab" in the UI
org = 'influxdata@bramderuyck.be'
# Your organization name is your e-mail address in the free version
bucket = "influxdata's Bucket"
# This is the standard bucket name
owner = "bdr"
# Your own first name


def send_to_influxdb():
	client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=my_token)
	try:
		kind = 'temperature'
		device = 'opt-123'
		"""
		Get sensor data
		"""
		# pressure = sense.get_pressure()
		pressure = 339.3
		# pressure = round(pressure, 1)
		temp = 12.0
		# temp = sense.get_temperature()
		# temp = round(temp, 1)
		# humid = sense.get_humidity()
		humid = 99

		"""
		Write data by Point structure
		"""
		point = Point(kind).tag('owner', owner).tag('device', device).field('value', round(outside_temp(), 2)).time(time=datetime.utcnow())
		print(f'Writing to InfluxDB cloud: {point.to_line_protocol()} ...')

		write_api = client.write_api(write_options=SYNCHRONOUS)
		write_api.write(bucket=bucket, org=org, record=point)

		print()
		print('success')
		print()
		print()

		if False:
			"""
			Query written data
			"""
			query = f'from(bucket: "{bucket}") |> range(start: -1d) |> filter(fn: (r) => r._measurement == "{kind}")'
			print(f'Querying from InfluxDB cloud: "{query}" ...')
			print()

			query_api = client.query_api()
			tables = query_api.query(query=query, org=org)

			for table in tables:
				for row in table.records:
					print(f'{row.values["_time"]}: owner={row.values["owner"]},device={row.values["device"]} '
						  f'{row.values["_value"]} °C')

			print()
			print('success')
	except Exception as e:
		print(e)
	finally:
		client.close()
	return


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


while True:
	send_to_influxdb()
	sleep(3.3)

