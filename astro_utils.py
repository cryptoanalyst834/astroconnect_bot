from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import datetime
from geopy.geocoders import Nominatim

def generate_natal_chart(date: str, time: str, location: str = 'Moscow'):
    geo = GeoPos('55.7558', '37.6176')  # Москва

    if location.lower() != 'moscow':
        try:
            geolocator = Nominatim(user_agent="astro_bot")
            loc = geolocator.geocode(location)
            if loc:
                geo = GeoPos(str(loc.latitude), str(loc.longitude))
        except:
            pass

    date_obj = Datetime(datetime.strptime(date, '%d.%m.%Y').strftime('%Y/%m/%d'), time, '+03:00')
    chart = Chart(date_obj, geo)
    return chart.get('SUN').sign, chart.get('ASC').sign
