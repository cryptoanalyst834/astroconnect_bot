from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import datetime
from geopy.geocoders import Nominatim

def generate_natal_chart(date: str, time: str, location: str = 'Moscow'):
    dt = datetime.strptime(f"{date} {time}", "%d.%m.%Y %H:%M")
    geo = GeoPos('55.7558', '37.6176')  # Москва

    if location and location.lower() != 'moscow':
        try:
            geolocator = Nominatim(user_agent="astro_bot")
            loc = geolocator.geocode(location)
            if loc:
                geo = GeoPos(str(loc.latitude), str(loc.longitude))
        except:
            pass

    date_obj = Datetime(dt.strftime('%Y/%m/%d'), dt.strftime('%H:%M'), '+03:00')
    chart = Chart(date_obj, geo)
    return chart.get('SUN').sign, chart.get('ASC').sign
