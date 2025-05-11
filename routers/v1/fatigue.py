import json
import random

from flask import Blueprint, jsonify

from clients.influx_client import InfluxClient
from clients.mqtt_client import MQTTClient
from utils.fatigue import calculate_fatigue

api_fatigue_router = Blueprint("api_fatigue_router", __name__)


@api_fatigue_router.route("/v1/fatigue", methods=["GET"])
def get_fatigule_by_latest():
    influx_client = InfluxClient("esp_bucket")
    # TODO: Получать данные с БД
    temp = 30
    co2 = 100
    heart_rate = 60
    spo2 = 90
    drive_time = 4.5
    age = 25
    gender = 'male'
    data = [
        temp,
        co2,
        heart_rate,
        spo2,
        drive_time,
        age,
        gender
    ]
    fatigue = calculate_fatigue(*data)

    response = {
        "data": fatigue,
    }

    return jsonify(response)
