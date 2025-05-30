#include <Arduino.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>

// Настройка UART для GPS (можно использовать UART1 или UART2)
#define GPS_RX_PIN 17  // Подключите RX GPS к этому пину ESP32-S3
#define GPS_TX_PIN 18  // Подключите TX GPS к этому пину ESP32-S3
#define GPS_BAUDRATE 9600  // Скорость обмена данными с GPS-модулем

HardwareSerial gpsSerial(1);  // Используем UART1
TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(GPS_BAUDRATE, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);

  Serial.println("GPS Test with ESP32-S3");
  Serial.println("Waiting for GPS data...");
}

void loop() {
  // Чтение данных из GPS
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      displayGPSData();
    }
  }

  // Если в течение 5 секунд нет данных, выводим ошибку
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println("No GPS detected. Check wiring.");
    while (true);  // Остановка программы
  }
}

void displayGPSData() {
  if (gps.location.isValid()) {
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
    Serial.print("Speed: ");
    Serial.print(gps.speed.kmph());  // Скорость в км/ч
    Serial.println(" km/h");
  } else {
    Serial.println("Location not valid");
  }

  Serial.print("Satellites: ");
  Serial.println(gps.satellites.value());

  Serial.println("---------------------");
  delay(1000);  // Задержка для удобства чтения
}