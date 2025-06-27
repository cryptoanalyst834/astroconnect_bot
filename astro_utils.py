from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

def calc_natal(date_str, time_str, place_lat, place_lon):
    dt = Datetime(date_str, time_str, "+03:00")  # поправьте на нужный TZ
    pos = GeoPos(place_lat, place_lon)
    chart = Chart(dt, pos)
    sun_sign = chart.get("SUN").sign
    asc_sign = chart.get("ASC").sign
    return sun_sign, asc_sign
