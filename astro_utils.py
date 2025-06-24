from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from geopy.geocoders import Nominatim

async def generate_natal_chart(date_str, time_str, city_name):
    geolocator = Nominatim(user_agent="astroconnect")
    location = geolocator.geocode(city_name, timeout=10)
    if location:
        lat = f"{location.latitude:.4f}"
        lon = f"{location.longitude:.4f}"
    else:
        lat = "55.7558"  # Москва
        lon = "37.6176"

    date_parts = date_str.split(".")
    year, month, day = int(date_parts[2]), int(date_parts[1]), int(date_parts[0])
    dt = Datetime(f"{year}-{month:02}-{day:02}", time_str, "+03:00")
    pos = GeoPos(lat, lon)
    chart = Chart(dt, pos)

    sun = chart.get("SUN")
    asc = chart.get("ASC")

    return {
        "zodiac": sun.sign,
        "ascendant": asc.sign
    }
