from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import SUN, ASC
from geopy.geocoders import Nominatim

def generate_astrology_data(birth_date: str, birth_time: str, birth_place: str):
    try:
        geolocator = Nominatim(user_agent="astro_bot")
        location = geolocator.geocode(birth_place)
        if not location:
            return None, None

        pos = GeoPos(str(location.latitude), str(location.longitude))
        dt = Datetime(birth_date, birth_time, "+03:00")
        chart = Chart(dt, pos)

        sun = chart.get(SUN)
        asc = chart.get(ASC)

        zodiac_sign = sun.sign
        ascendant = asc.sign
        return zodiac_sign, ascendant

    except Exception as e:
        print(f"Error in astrology generation: {e}")
        return None, None
