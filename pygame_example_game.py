"""
Программа pygame для демонстрации запросов на сервер.
Перед запуском игры убедитесь, что сервер работает.
"""
import json
import random

import pygame
import requests

import configparser

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from dotenv import load_dotenv

load_dotenv()
config = configparser.ConfigParser()
config.read('config.ini')

token = os.environ.get("INFLUXDB_TOKEN")
org = os.getenv("INFLUX_ORG")
url = config.get('APP', 'INFLUX_URL')

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "esp_bucket"
write_api = write_client.write_api(write_options=SYNCHRONOUS)


import paho.mqtt.client as mqtt
import time
import random

MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensors/temperature"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

while True:
    temperature = random.uniform(20.0, 30.0)  # Имитация датчика
    client.publish(MQTT_TOPIC, f"{temperature:.2f}")
    print(f"Отправлено: {temperature:.2f}°C")
    time.sleep(2)  # Пауза 2 секунды

class Settings:
    WIDTH = 600
    HEIGHT = 400

    @property
    def window_center(self):
        return self.WIDTH // 2

    @staticmethod
    def window_size():
        return [Settings.WIDTH, Settings.HEIGHT]


class BaseButtonAction:
    """
    Стратегия, алгоритмы для нажания на кнопку
    """

    def execute(self):
        raise NotImplementedError("Не реализован метод")


class NothingButtonAction(BaseButtonAction):
    def execute(self):
        pass


class WinButtonAction(BaseButtonAction):
    def execute(self):
        data = {
            "username": "KriptYashka"
        }
        response = requests.get("http://localhost:8000/api/win/", data=data)


class GetMoneyButtonAction(BaseButtonAction):
    def execute(self):
        data = {
            "username": "KriptYashka"
        }
        response = requests.get("http://localhost:8000/api/money/", data=data)
        response_data = response.json()
        money = response_data["money"]
        return money


class Button:
    def __init__(self, rect: list, action_name: str):
        self.rect = pygame.rect.Rect(*rect)
        self.color = [200, 20, random.randint(50, 200)]
        self.action = self.select_action(action_name)

    def select_action(self, action_name: str):
        action_name = action_name.lower()
        actions = {
            "nothing": NothingButtonAction,
            "win": WinButtonAction,
            "money": GetMoneyButtonAction
        }
        if action_name not in actions:
            raise Exception(f"Действия {action_name} нет в словаре")
        return actions[action_name]

    def event(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.action().execute()

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode(Settings.window_size())

    btn_actions = ["nothing", "win", "money"]
    btn_size = [300, 100]
    buttons = []

    for i in range(3):
        rect = [
            Settings.WIDTH // 2 - btn_size[0] // 2,
            25 + i * (btn_size[1] + 20),
            btn_size[0],
            btn_size[1]
        ]
        btn = Button(rect, btn_actions[i])
        buttons.append(btn)

    gameover = False
    while not gameover:
        # Событие
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in buttons:
                        btn.event()  # Проверка, что нажали именно на эту кнопку
        # Логика (её нет)
        ...
        # Отрисовка
        screen.fill([20] * 3)

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        pygame.time.delay(20)


if __name__ == "__main__":
    main()
