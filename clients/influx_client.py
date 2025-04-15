import os

from influxdb_client.client import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from settings import Settings


class InfluxClient:
    __CLIENT = None
    __bucket = None
    __org = None

    def __new__(cls, bucket: str):
        if cls.__CLIENT is None:
            config = Settings.CONFIG
            token = os.getenv("INFLUXDB_TOKEN")
            org = os.getenv("INFLUX_ORG")
            url = config.get('APP', 'INFLUX_URL')

            cls.__CLIENT = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
            cls.__bucket = bucket
            cls.__org = org
        return object.__new__(cls)

    def post(self, record):
        write_qpi = self.__CLIENT.write_api(write_options=SYNCHRONOUS)
        write_qpi.write(self.__bucket, self.__org, record)
