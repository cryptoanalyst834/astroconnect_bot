from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.const import SUN, ASC
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode_place(city_name):
    """Геокодинг города — получает координаты по названию"""
    geolocator = Nominatim(user_agent="astroconnect")
    try:
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return {"lat": location.latitude, "lon": location.longitude}
    except GeocoderTimedOut:
        pass
    # Fallback: Москва
    return {"lat": 55.7558, "lon": 37.6176}

def get_zodiac_and_ascendant(date: str, time: str, city: str = "Москва"):
    pos = geocode_place(city)
    dt = Datetime(date, time)
    chart = Chart(dt, pos)
    sun_sign = chart.get(SUN).sign
    asc_sign = chart.get(ASC).sign
    return sun_sign, asc_sign

def compatibility_score(profile1, profile2):
    # Пример: если совпадает хотя бы один знак — +50%, иначе 0
    score = 0
    if profile1["zodiac"] == profile2["zodiac"]:
        score += 50
    if profile1["ascendant"] == profile2["ascendant"]:
        score += 50
    return score
