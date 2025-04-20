import json
import random

from flask import Blueprint, jsonify

from clients.mqtt_client import MQTTClient

api_router = Blueprint("api_router", __name__)


@api_router.route("/v1/sensor/temperature", methods=["GET", "POST"])
def sensor_temperature():
    mqtt_client = MQTTClient()
    temp = random.random() * 10 + 20

    response = {
        "temperature": temp
    }

    mqtt_client.publish("sensor/temperature", json.dumps(response))

    return jsonify(response)

