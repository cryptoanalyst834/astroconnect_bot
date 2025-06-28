from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import SUN, ASC

def calc_chart(date_str, time_str, place_lat, place_lon):
    dt = Datetime(f"{date_str}", f"{time_str}")
    pos = GeoPos(place_lat, place_lon)
    chart = Chart(dt, pos)
    zodiac = chart.get(SUN).sign
    ascendant = chart.get(ASC).sign
    return zodiac, ascendant
