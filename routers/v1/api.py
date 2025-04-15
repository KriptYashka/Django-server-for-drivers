import random

from flask import Blueprint

from clients.mqtt_client import MQTTClient

api_router = Blueprint("api_router", __name__)


@api_router.route("/v1/sensor/temperature", methods=["GET", "POST"])
def sensor_temperature():
    mqtt_client = MQTTClient()
    temp = random.random() * 10 + 20
    mqtt_client.publish("sensor/temperature", temp)
    return f"Температура: {temp}"

