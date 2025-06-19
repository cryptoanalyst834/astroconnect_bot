# astro_utils.py

from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

def generate_astrology_info(data):
    birth_date = data['birth_date']  # формат дд.мм.гггг
    birth_time = data['birth_time']  # формат чч:мм
    date_parts = birth_date.split(".")
    time_parts = birth_time.split(":")

    dt = Datetime(f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}",
                  f"{time_parts[0]}:{time_parts[1]}", '+03:00')

    # пока жестко — Москва. Позже подключим геокодер
    pos = GeoPos("55.7558", "37.6173")

    chart = Chart(dt, pos)
    sun_sign = chart.get(const.SUN).sign
    asc = chart.get(const.ASC).sign
    return sun_sign, asc
