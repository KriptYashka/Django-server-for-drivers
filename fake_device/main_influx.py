import configparser

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from dotenv import load_dotenv

load_dotenv()
config = configparser.ConfigParser()
config.read('config.ini')

token = os.environ.get("INFLUXDB_TOKEN")
org = os.getenv("INFLUX_ORG")
url = config.get('APP', 'INFLUX_URL')

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "esp_bucket"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = (
        Point("measurement1")
        .tag("tagname1", "tagvalue1")
        .field("field1", value)
    )
    write_api.write(bucket=bucket, org="No", record=point)
    time.sleep(1)  # separate points by 1 second

query_api = write_client.query_api()

query = """from(bucket: "esp_bucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="No")

for table in tables:
    for record in table.records:
        print(record)
