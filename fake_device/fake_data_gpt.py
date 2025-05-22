import json
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import random
import time

# Конфигурация
from utils.fatigue import calculate_fatigue

MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensor/health"
START_TIME = datetime(2025, 5, 21, 20, 48)
END_TIME = datetime(2025, 5, 21, 21, 32)
INTERVAL = timedelta(seconds=10)

client = mqtt.Client()
client.connect(MQTT_BROKER)


def generate_data(timestamp, progress):
    co2 = 100 + random.uniform(-2, 0)

    if progress < 0.3:
        heart_rate = 80 + random.uniform(-10, 10)
        if random.random() < 0.1:
            heart_rate = 100 + random.uniform(0, 10)
    else:
        heart_rate = 70 - progress * 30 * (random.random() / 2 + 0.6)

    spo2 = 90 + random.uniform(-1, 10)
    if random.random() < 0.05:
        spo2 = 0

    temperature = 30 + random.uniform(-2, 2)

    temp = temperature
    co2 = co2
    heart_rate = heart_rate
    spo2 = spo2
    drive_time = 2 + progress
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

    return {
        "time": timestamp.isoformat() + "Z",
        "fields": {
            "co2": max(85, min(100, co2)),
            "heart_rate": max(40, min(120, heart_rate)),
            "spo2": spo2,
            "temperature": temperature,
            "fatigue": fatigue * 100,
        },
        "tags": {
            "device": "esp",
            "location": "outdoor"
        }
    }


current_time = START_TIME
while current_time <= END_TIME:
    progress = (current_time - START_TIME) / (END_TIME - START_TIME)
    data = generate_data(current_time, progress)

    # Формат совместимый с Telegraf+Influx
    payload = {
        "measurement": "health_metrics",
        "tags": data["tags"],
        "time": data["time"],
        "fields": data["fields"]
    }

    client.publish(MQTT_TOPIC, json.dumps(payload))
    print(f"Sent: {current_time} | HR: {data['fields']['heart_rate']:.1f}")

    current_time += INTERVAL
    time.sleep(0.01)  # Минимальная пауза

client.disconnect()