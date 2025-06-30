from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.const import SUN, ASC

def get_zodiac_and_ascendant(date: str, time: str):
    # date: "YYYY-MM-DD", time: "HH:MM"
    dt = Datetime(date, time)
    # Координаты Москвы — по умолчанию
    pos = {"lat": "55.7558", "lon": "37.6176"}
    chart = Chart(dt, pos)
    sun_sign = chart.get(SUN).sign
    asc_sign = chart.get(ASC).sign
    return sun_sign, asc_sign

def compatibility_score(profile1, profile2):
    """Заглушка логики совместимости"""
    score = 0
    if profile1.get("zodiac") == profile2.get("zodiac"):
        score += 50
    if profile1.get("ascendant") == profile2.get("ascendant"):
        score += 50
    return score
