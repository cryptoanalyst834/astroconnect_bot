from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from geopy.geocoders import Nominatim

async def generate_astrology_data(birth_date: str, birth_time: str, birth_place: str):
    # Объединяем дату и время
    date_parts = birth_date.split(".")
    day, month, year = map(int, date_parts)
    time_parts = birth_time.split(":")
    hour, minute = map(int, time_parts)

    # Геопозиция
    geolocator = Nominatim(user_agent="astro_bot")
    location = geolocator.geocode(birth_place)
    if not location:
        raise ValueError("Не удалось найти координаты места рождения")

    pos = GeoPos(str(location.latitude), str(location.longitude))
    date = Datetime(f"{year}-{month:02d}-{day:02d}", f"{hour:02d}:{minute:02d}", "+03:00")

    chart = Chart(date, pos)
    sun = chart.get("SUN")
    asc = chart.get("ASC")

    return {
        "zodiac_sign": sun.sign,
        "ascendant": asc.sign
    }
