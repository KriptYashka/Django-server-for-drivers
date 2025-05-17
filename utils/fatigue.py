"""
Модуль вычисления усталости пилота
"""


def calculate_fatigue(
    temp: float,
    co2: float,
    heart_rate: float,
    spo2: float,
    drive_time: float,
    age: int,
    gender: str = 'male'
) -> float:
    """
    Определяет коэффициент усталости

    :param temp: Температура окружающей среды (салона)
    :param co2: Содержание углекислого газа в среде (салон)git
    :param heart_rate: Пульс пилота
    :param spo2: Уровень кислорода в крови
    :param drive_time: Время полёта/поездки
    :param age: Возраст пилота
    :param gender: Пол пилота

    :return: Коэффициент усталости от 0 до 1
    """
    norm_temp = max(0.0, min(1.0, (temp - 20) / 15))  # 20°C - комфортная, 35°C - макс
    norm_co2 = co2 / 100
    norm_hr = max(0.0, min(1.0, (heart_rate - 60) / 60))  # 60-70 - норма, >100 - стресс
    norm_spo2 = (100 - spo2) / 10  # 90%-100% → 0..1
    norm_time = max(0.0, min(1.0, drive_time / 360))  # 6 часов = 1

    age_factor = min(1.0, age / 60) * 0.1  # старше 60 лет — чуть больше влияния
    # Влияние пола (примерно: женщины более чувствительны к снижению SpO2)
    gender_factor = 0.05 if gender == 'female' else 0

    fatigue = (
                      norm_temp * 0.1 +
                      norm_co2 * 0.2 +
                      norm_hr * 0.2 +
                      norm_spo2 * 0.25 +
                      norm_time * 0.25
              ) + age_factor + gender_factor

    return round(min(1.0, max(0.0, fatigue)), 2)
