import configparser

import paho.mqtt.client as mqtt
import time
import random

config = configparser.ConfigParser()
config.read("config.ini")

MQTT_BROKER = config.get("APP", "MQTT_BROKER")
MQTT_TOPIC = "sensors/temperature"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

while True:
    temperature = random.uniform(20.0, 30.0)  # Имитация датчика
    client.publish(MQTT_TOPIC, f"{temperature:.2f}")
    print(f"Отправлено: {temperature:.2f}°C")
    time.sleep(2)  # Пауза 2 секунды