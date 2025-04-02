# ESP32-S3 API Server

Сервер для проекта мониторинга усталости водителей

---

# Запуск сервиса

1. С помощью Docker запустить сервер

```bash
sudo docker run -d -p 8086:8086 -v "$PWD/data:/var/lib/influxdb2" -v "$PWD/config:/etc/influxdb2" influxdb:2
```

2. Установить виртуальное окружение и библиотеки

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Продолжение следует