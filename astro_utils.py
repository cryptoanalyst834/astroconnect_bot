from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geo import Geo
from geopy.geocoders import Nominatim

def geocode_place(place: str):
    geolocator = Nominatim(user_agent="AstroConnect")
    location = geolocator.geocode(place)
    if not location:
        raise ValueError("Место рождения не найдено.")
    return location.latitude, location.longitude

def get_zodiac_and_ascendant(date, time, place):
    latitude, longitude = geocode_place(place)
    dt = Datetime(date.strftime("%Y/%m/%d"), time.strftime("%H:%M"))
    geo = Geo(place, latitude, longitude)
    chart = Chart(dt, geo)
    zodiac = chart.sun.sign
    ascendant = chart.asc.sign
    return zodiac, ascendant, chart.aspects

def calc_compatibility(chart1: dict, chart2: dict) -> float:
    # Пример: простая совместимость по знакам
    return 1.0 if chart1['zodiac'] == chart2['zodiac'] else 0.5
