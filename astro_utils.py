from flatlib.geo import Geo
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from geopy.geocoders import Nominatim

def geocode_place(place):
    geolocator = Nominatim(user_agent="astroconnect")
    location = geolocator.geocode(place)
    if location:
        return location.longitude, location.latitude
    else:
        raise ValueError("Город не найден")

def get_natal_chart(date_str, time_str, place):
    lon, lat = geocode_place(place)
    dt = Datetime(f"{date_str}", f"{time_str}", '+03:00')
    pos = Geo('', lon, lat)
    chart = Chart(dt, pos)
    return chart

def get_zodiac_and_ascendant(chart):
    sun = chart.get('SUN')
    asc = chart.get('ASC')
    return sun.sign, asc.sign
