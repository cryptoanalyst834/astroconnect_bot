from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geo import Geo
from flatlib import const

from geopy.geocoders import Nominatim

def geocode_place(place: str):
    geolocator = Nominatim(user_agent="astroconnect")
    location = geolocator.geocode(place)
    if not location:
        raise ValueError("Место не найдено")
    return location.latitude, location.longitude

def get_zodiac_and_ascendant(date, time, lat, lon):
    dt = Datetime(f"{date}", f"{time}")
    geo = Geo(lat, lon)
    chart = Chart(dt, geo)
    sun = chart.get(const.SUN)
    asc = chart.get(const.ASC)
    return sun.sign, asc.sign
