import json
import random
import requests


def fetch_json(url):
    """Fetch JSON from url."""
    response = requests.get(url)
    if not 200 <= response.status_code <= 299:
        raise Exception(f'[HTTP - {response.status_code}]: {response.reason}')
    config_fresh = json.loads(response.content.decode('utf-8'))
    return config_fresh


class Sensor:
    def __init__(self):
        self.id = ''
        self.temperature = None
        self.pressure = None
        self.humidity = None

    def generate_measurement(self):
        return round(random.uniform(0, 100))

    def geo(self):
        """
        Получает геопозицию с https://freegeoip.app/json/'.
        :return: Словарь с долготой и широтой
        """
        try:
            return fetch_json('https://freegeoip.app/json/')
        except Exception:
            return {
                'latitude':  self.generate_measurement(),
                'longitude':  self.generate_measurement(),
            }