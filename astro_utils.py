from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.const import SUN, ASC

def get_zodiac_and_ascendant(date: str, time: str):
    # date: "YYYY-MM-DD", time: "HH:MM"
    dt = Datetime(date, time)
    # Пример координат для Москвы (можно всегда их ставить, если город не вводится)
    pos = {"lat": "55.7558", "lon": "37.6176"} 
    chart = Chart(dt, pos)
    sun_sign = chart.get(SUN).sign
    asc_sign = chart.get(ASC).sign
    return sun_sign, asc_sign
