import paho.mqtt.client as mqtt
import paho.mqtt.publish as p
from settings import Settings


class MQTTClient:
    __CLIENT = None

    def __new__(cls, *args, **kwargs):
        if cls.__CLIENT is None:
            cls.__CLIENT = mqtt.Client()
        mqtt_broker = Settings.CONFIG.get("APP", "MQTT_BROKER")
        cls.__CLIENT.connect(mqtt_broker, 1883, 5)
        return object.__new__(cls)

    def publish(self, topic: str, *args, **kwargs):
        self.__CLIENT.publish(topic, *args, **kwargs)
#
# while True:
#     temperature = random.uniform(20.0, 30.0)  # Имитация датчика
#     client.publish(MQTT_TOPIC, f"{temperature:.2f}")
#     print(f"Отправлено: {temperature:.2f}°C")
#     time.sleep(2)  # Пауза 2 секунды
