from geopy.geocoders import Nominatim
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.const import SUN, ASC

def geocode_place(city: str):
    geolocator = Nominatim(user_agent="astroconnect")
    location = geolocator.geocode(city)
    if location:
        return float(location.latitude), float(location.longitude)
    # Default to Moscow
    return 55.7558, 37.6176

def get_zodiac_and_ascendant(date: str, time: str, city: str):
    lat, lon = geocode_place(city)
    dt = Datetime(date, time)
    pos = {"lat": str(lat), "lon": str(lon)}
    chart = Chart(dt, pos)
    sun_sign = chart.get(SUN).sign
    asc_sign = chart.get(ASC).sign
    return sun_sign, asc_sign
