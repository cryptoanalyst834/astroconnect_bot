from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
import sys
import json

birth_date = sys.argv[1]  # format: YYYY-MM-DD
birth_time = sys.argv[2]  # format: HH:MM
birth_place = sys.argv[3]  # e.g., "Moscow"

# Stub: можно заменить на реальный геокодинг
coords = {
    "Moscow": GeoPos("55.7558", "37.6173"),
    "New York": GeoPos("40.7128", "-74.0060"),
}

pos = coords.get(birth_place, GeoPos("55.7558", "37.6173"))

dt = Datetime(birth_date, birth_time, "+03:00")
chart = Chart(dt, pos)

result = {obj.id: {"sign": obj.sign, "lon": obj.lon} for obj in chart.objects}
print(json.dumps(result))
