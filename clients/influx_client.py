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

    def get(self, topic: str, time_before: int = 1):
        query_api = self.__CLIENT.query_api()
        query = f"""
            from(bucket: "{self.__bucket}")
              |> range(start: -{time_before}h)
              |> filter(fn: (r) => r["topic"] == "{topic}")
        """
        print("Query: ", query)
        result = query_api.query(query)
        return result

    def post(self, record):
        write_api = self.__CLIENT.write_api(write_options=SYNCHRONOUS)
        write_api.write(self.__bucket, self.__org, record)
