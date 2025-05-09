import json
import random

from flask import Blueprint, jsonify

from clients.influx_client import InfluxClient
from clients.mqtt_client import MQTTClient

api_router = Blueprint("api_router", __name__)


@api_router.route("/v1/sensor/p/temperature", methods=["GET"])
def sensor_publish_random_temperature():
    mqtt_client = MQTTClient()
    temp = random.random() * 10 + 20

    response = {
        "temperature": temp
    }

    mqtt_client.publish("sensor/temperature", json.dumps(response))

    return jsonify(response)


@api_router.route("/v1/sensor/<sensor_name>", methods=["GET", "POST"])
def sensor_temperature(sensor_name: str):
    """
    Обращается к InfluxDB, выводит информацию о температуре за последний час
    """
    influxdb_client = InfluxClient("esp_bucket")
    result = influxdb_client.get(f"sensor/{sensor_name}")
    print(result)

    data = []

    for table in result:
        for record in table.records:
            print(
                f"Time: {record.get_time()}, Measurement: {record.get_measurement()}, Field: {record.get_field()}, Value: {record.get_value()}")
            data.append({
                "time": record.get_time(),
                record.get_field(): record.get_value(),
            })

    response = {
        "data": data
    }

    return jsonify(response)
