"""
Connect to InfluxDB 2.0 - write data and query them
"""

from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from random import uniform
from time import sleep

my_token = "D6ltGUKEgdSCOU9FgswD6Zp6H8faQ7MsdEE3JevpmTN-32JJSdATdyNfCOb_6SguWeAzd29NkFd6iid-mYfX9g=="
## You can generate a Token from the "Tokens Tab" in the UI
org = 'influxdata@bramderuyck.be'
# Your organization name is your e-mail address in the free version
bucket = "influxdata's Bucket"
# This is the standard bucket name


def send_basic():
	client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=my_token)
	try:
		kind = 'temperature'
		host = 'host1'
		device = 'opt-123'
		"""
		Write data by Point structure
		"""
		point = Point(kind).tag('host', host).tag('device', device).field('value', uniform(23.0, 27.0)).time(time=datetime.utcnow())
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
					print(f'{row.values["_time"]}: host={row.values["host"]},device={row.values["device"]} '
						  f'{row.values["_value"]} °C')

			print()
			print('success')
	except Exception as e:
		print(e)
	finally:
		client.close()
	return


while True:
	send_basic()
	sleep(1)