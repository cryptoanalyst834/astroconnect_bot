from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

def generate_natal_chart(date_str, time_str, city):
    # В проде подключить геокодинг через API или использовать словарь
    pos = GeoPos("55n45", "37e35")  # Москва по умолчанию
    date_parts = date_str.split(".")
    year, month, day = int(date_parts[2]), int(date_parts[1]), int(date_parts[0])
    dt = Datetime(f"{year}-{month:02}-{day:02}", time_str, "+03:00")

    chart = Chart(dt, pos)
    sun = chart.get("SUN")
    asc = chart.get("ASC")

    return {
        "zodiac": sun.sign,
        "ascendant": asc.sign
    }
