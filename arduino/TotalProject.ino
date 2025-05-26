#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

/* Heart rate and SpO2 */
MAX30105 particleSensor;
const byte RATE_SIZE = 4;

/* mqtt */
WiFiClient espClient;
PubSubClient client(espClient);

const char* mqtt_topic = "sensor"; // Топик для публикации
const char* mqtt_server = "192.168.1.77";
  const int mqtt_port = 1883; // Стандартный порт MQTT

class MQTTController{
  const char* ssid = "MGTS_GPON_82F1"; //тут название вай-фай сети
  const char* password = "UY5RQ7FC"; //тут пароль вай-фай сети

  public:
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

    client.setServer(mqtt_server, mqtt_port);
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

  void sendDictOverMQTT(const char* topic, JsonDocument& dict) {
    if (!client.connected()) {
      reconnect();
    }

    String jsonStr;
    serializeJson(dict, jsonStr);

    if (client.publish(topic, jsonStr.c_str())) {
      Serial.print("Успешно отправлено в ");
      Serial.print(topic);
      Serial.print(": ");
      Serial.println(jsonStr);
    } else {
      Serial.println("Ошибка отправки MQTT сообщения");
    }
  }


};

class HeartSensor {
    long irValue;
    byte rates[RATE_SIZE];
    byte rateSpot = 0;
    long lastBeat = 0;

    float beatsPerMinute;
    int beatAvg;

  public:
    HeartSensor() {
      irValue = 0;
      for (byte x = 0; x < RATE_SIZE; x++)
        rates[x] = 0;
    }

    void setup() {
      // Инициализация I2C с явным указанием пинов и пониженной скоростью
      Wire.begin(8, 9);  // SDA=GPIO8, SCL=GPIO9 для ESP32-S3
      Wire.setClock(100000);  // Понижаем скорость до 100 kHz

      // Попытка инициализации с повторными попытками
      int attempts = 0;
      while (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
        attempts++;
        Serial.printf("Попытка %d: MAX30105 не найден! Проверьте подключение.\n", attempts);
        if (attempts >= 5) {
          Serial.println("Превышено количество попыток. Пожалуйста, проверьте:");
          Serial.println("1. Подключение SDA(8), SCL(9)");
          Serial.println("2. Питание датчика (3.3V)");
          Serial.println("3. Пульсацию светодиодов датчика");
          while (1) {
            delay(1000);
            Serial.print(".");
          }
        }
        delay(500);
      }

      Serial.println("Датчик MAX30105 инициализирован успешно!");

      // Более безопасная настройка
      byte ledBrightness = 0x1F;  // Средняя яркость
      byte sampleAverage = 4;
      byte ledMode = 2;  // Красный + ИК
      int sampleRate = 400;
      int pulseWidth = 411;
      int adcRange = 4096;

      particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
      particleSensor.enableDIETEMPRDY();

      // Включаем только необходимые светодиоды
      particleSensor.setPulseAmplitudeRed(0x0A);
      particleSensor.setPulseAmplitudeGreen(0x00);
      particleSensor.setPulseAmplitudeProximity(0x00);
    }



    void process_beat() {
      irValue = particleSensor.getIR();
      if (irValue == 0){
        particleSensor.begin(Wire, I2C_SPEED_STANDARD);
        delay(500);
        return;
      }
      if (checkForBeat(irValue)) {
        long delta = millis() - lastBeat;
        lastBeat = millis();

        beatsPerMinute = 60 / (delta / 1000.0);

        if (beatsPerMinute < 255 && beatsPerMinute > 20) {
          rates[rateSpot++] = (byte)beatsPerMinute;
          rateSpot %= RATE_SIZE;

          beatAvg = 0;
          for (byte x = 0; x < RATE_SIZE; x++)
            beatAvg += rates[x];
          beatAvg /= RATE_SIZE;
        }
      }
    }

    float get_avg_bpm(){
      return beatAvg;
    }

    float get_spo2(){
      return 100;
    }

    void show() {
      Serial.println("# Heart #");
      Serial.print("IR=");
      Serial.print(irValue);
      Serial.print(", BPM=");
      Serial.print(beatsPerMinute);
      Serial.print(", Avg BPM=");
      Serial.print(beatAvg);

      if (irValue < 50000)
        Serial.print(" No finger?");

      Serial.println();
    }
};

class CO2Sensor {
  private:
  const int mq2AnalogPin = 2;
  const int mq2DigitalPin = 4;
  const int dangerLedPin = 5;
  int digitalValue;
  int analogValue;
  long lastMillis;
  long delay = 1000;

  public:
  void setup(){
    pinMode(mq2AnalogPin, INPUT);
    pinMode(mq2DigitalPin, INPUT);
    pinMode(dangerLedPin, OUTPUT);  // Сигнал опасности
    lastMillis = millis();
  }

  void process(){
    if (millis() - lastMillis >= delay){
      lastMillis = millis();
      analogValue = analogRead(mq2AnalogPin);
      digitalValue = digitalRead(mq2DigitalPin);

      if (analogValue < 200) {
        digitalWrite(dangerLedPin, HIGH);
      } else {
        digitalWrite(dangerLedPin, LOW);
      }
    }
  }

  float get_co2_norm(){
    float min = 100;
    float max = 500;

    float value = (analogValue - min) / max * 100.0;
    // if (value > 100){
    //   value = 100;
    // } else if (value < 0){
    //   value = 0;
    // }
    return value;
  }

  void show(){
    Serial.println("# CO2 #");
    Serial.print("Analog: ");
    Serial.print(analogValue);
    Serial.print("; Digital: ");
    Serial.println(digitalValue);
  }
};

HeartSensor heart_sensor;
CO2Sensor co2_sensor;
MQTTController mqtt;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Initializing...");

  /* Heart rate and SpO2 */
  heart_sensor.setup();
  co2_sensor.setup();

  mqtt.setup_wifi();
}

void loop() {
  heart_sensor.process_beat();
  co2_sensor.process();

  heart_sensor.show();
  co2_sensor.show();

  StaticJsonDocument<200> sensorData;
  sensorData["device"] = "ESP32-S3";

  sensorData["heart_rate"] = heart_sensor.get_avg_bpm();
  sensorData["spo2"] = heart_sensor.get_spo2();
  sensorData["temperature"] = (float)temperatureRead();
  sensorData["co2"] = co2_sensor.get_co2_norm();

  mqtt.sendDictOverMQTT(mqtt_topic, sensorData);
  delay(10);
}
