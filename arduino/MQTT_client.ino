#include <WiFi.h>
#include <PubSubClient.h>
#include <stdlib.h> // Для работы с random()

// Настройки Wi-Fi
const char* ssid = "MGTS_GPON_82F1"; //тут название вай-фай сети
const char* password = "UY5RQ7FC"; //тут пароль вай-фай сети

// Настройки MQTT
const char* mqtt_server = "192.168.1.77";
const int mqtt_port = 1883; // Стандартный порт MQTT
const char* mqtt_topic = "esp32s3/random"; // Топик для публикации

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Подключение к ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi подключен");
  Serial.println("IP адрес: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Повторное подключение к MQTT-серверу
  while (!client.connected()) {
    Serial.print("Попытка подключения к MQTT...");

    // Создаем случайный client ID
    String clientId = "ESP32S3Client-";
    clientId += String(random(0xffff), HEX);

    // Пробуем подключиться
    if (client.connect(clientId.c_str())) {
      Serial.println("подключено");
    } else {
      Serial.print("ошибка, rc=");
      Serial.print(client.state());
      Serial.println(" пробуем снова через 5 секунд");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  randomSeed(analogRead(0)); // Инициализация генератора случайных чисел
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Генерируем случайное значение (от 0 до 1000)
  int randomValue = random(1000);

  // Конвертируем в строку
  char randomStr[10];
  itoa(randomValue, randomStr, 10);

  // Публикуем в MQTT
  client.publish(mqtt_topic, randomStr);
  Serial.print("Отправлено случайное значение: ");
  Serial.println(randomStr);

  delay(5000); // Отправляем каждые 5 секунд
}
