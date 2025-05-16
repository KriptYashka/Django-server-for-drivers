import configparser
import json

import paho.mqtt.client as mqtt
import time
import random

config = configparser.ConfigParser()
config.read("config.ini")

MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensor/temperature"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

while True:
    temperature = random.uniform(20.0, 30.0)
    co2 = random.uniform(75.0, 95.0)
    heart_rate = random.uniform(40.0, 120.0)
    spo2 = random.uniform(80.0, 100.0)

    data = {
        "temperature": temperature,
        "co2": co2,
        "heart_rate": heart_rate,
        "spo2": spo2
    }

    client.publish("sensor", json.dumps(data))

    print(f"Отправлено: {temperature:.2f}°C")
    time.sleep(5)