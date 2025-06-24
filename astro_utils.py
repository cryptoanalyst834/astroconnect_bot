from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

def get_natal_chart(date_str, time_str, lat, lon):
    date = Datetime(f'{date_str}', f'{time_str}')
    pos = GeoPos(lat, lon)
    return Chart(date, pos)
