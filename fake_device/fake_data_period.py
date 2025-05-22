import configparser
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime, timedelta
import random

from utils.fatigue import calculate_fatigue

start_time = datetime(2025, 5, 21, 20, 30)
end_time = datetime(2025, 5, 21, 21, 30)
current_time = start_time

client = mqtt.Client()
client.connect("localhost", 1883, 60)


def generate_data(current_time, progress):
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
        "time": current_time.isoformat() + "Z03:00",
        "fields": {
            "co2": round(co2, 2),
            "heart_rate": round(heart_rate, 2),
            "spo2": round(spo2, 2),
            "temperature": round(temperature, 2),
            "fatigue": fatigue * 100,
        },
        "tags": {
            "device": "esp",
            "location": "outdoor"
        }

    }


while current_time <= end_time:
    total_duration = (end_time - start_time).total_seconds()
    elapsed = (current_time - start_time).total_seconds()
    progress = elapsed / total_duration

    data = generate_data(current_time, progress)

    payload = {
        "measurement": "health_metrics",
        "tags": data["tags"],
        "time": data["time"],
        "fields": data["fields"]
    }

    client.publish("sensor", json.dumps(payload))

    print(f"[{current_time.strftime('%H:%M:%S')}] Отправлено: {json.dumps(payload)}")
    current_time += timedelta(seconds=20)
    time.sleep(0.01)

client.disconnect()
print("Генерация данных завершена")