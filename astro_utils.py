import asyncio
import logging
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)

# Создаём geolocator с таймаутом
geolocator = Nominatim(user_agent="astroconnect", timeout=10)

async def get_coordinates(city_name: str):
    try:
        location = await asyncio.to_thread(geolocator.geocode, city_name)
        if location:
            lat = f"{location.latitude:.4f}"
            lon = f"{location.longitude:.4f}"
            logger.info(f"Геокодинг для {city_name}: {lat}, {lon}")
            return lat, lon
        else:
            logger.warning(f"Город не найден: {city_name}, используется Москва")
            return "55.7558", "37.6176"
    except Exception as e:
        logger.error(f"Ошибка геокодинга: {e}")
        return "55.7558", "37.6176"

async def generate_natal_chart(date_str, time_str, city_name):
    lat, lon = await get_coordinates(city_name)
    try:
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
    except Exception as e:
        logger.error(f"Ошибка расчёта натальной карты: {e}")
        raise
