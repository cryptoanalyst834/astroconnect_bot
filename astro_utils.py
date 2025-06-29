from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geo import Geo
from flatlib import const
from geopy.geocoders import Nominatim

def geocode_place(place: str):
    geolocator = Nominatim(user_agent="astroconnect")
    location = geolocator.geocode(place, timeout=10)
    if not location:
        # fallback to Moscow
        return 55.751244, 37.618423
    return location.latitude, location.longitude

def get_zodiac_and_ascendant(date, time, place, lat, lon):
    dt = Datetime(date, time)
    geo = Geo(place, lat, lon)
    chart = Chart(dt, geo, IDs=const.LIST_OBJECTS)
    zodiac = chart.sun.sign
    ascendant = chart.ASC.sign
    return zodiac, ascendant, chart

def compatibility_score(chart1, chart2):
    # Более сложная логика совместимости: совпадение солнца/асцендента и разность по градусам солнца
    score = 0
    if chart1.sun.sign == chart2.sun.sign:
        score += 2
    if chart1.ASC.sign == chart2.ASC.sign:
        score += 1
    sun_diff = abs(chart1.sun.lon - chart2.sun.lon)
    score += max(0, 1 - sun_diff / 180)  # ближе - лучше
    return score
