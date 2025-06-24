from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# Здесь config не нужен, но при желании можно
# импортировать таймзону или прочие константы

def generate_astrology_data(date_str: str, time_str: str, place: str):
    date_parts = date_str.split(".")
    dt = Datetime(
        f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}",
        time_str,
        "+03:00",    # можно тоже вынести в config.TZ
    )
    pos = GeoPos(*get_coordinates(place))
    chart = Chart(dt, pos)
    return {
        "zodiac_sign": chart.get("SUN").sign,
        "ascendant": chart.get("ASC").sign
    }
