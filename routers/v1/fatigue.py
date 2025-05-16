import json
import logging
import random

from flask import Blueprint, jsonify

from clients.influx_client import InfluxClient
from clients.mqtt_client import MQTTClient
from utils.fatigue import calculate_fatigue

api_fatigue_router = Blueprint("api_fatigue_router", __name__)


@api_fatigue_router.route("/v1/fatigue/hour", methods=["GET"])
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


@api_fatigue_router.route("/v1/fatigue/now", methods=["GET"])
def get_fatigule_now():
    last_time = 5
    influx_client = InfluxClient("esp_bucket")
    temp = influx_client.get("temperature", last_time)[-1].records[-1].get_value()
    co2 = influx_client.get("co2", last_time)[-1].records[-1].get_value()
    heart_rate = influx_client.get("heart_rate", last_time)[-1].records[-1].get_value()
    spo2 = influx_client.get("spo2", last_time)[-1].records[-1].get_value()

    drive_time = 2

    age = 23
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

    data = {
        "fatigue": fatigue * 100
    }
    mqtt_client = MQTTClient()
    mqtt_client.publish("sensor", json.dumps(data))

    response = {
        "data": json.dumps(data),
        "result": fatigue * 100
    }

    return jsonify(response)
