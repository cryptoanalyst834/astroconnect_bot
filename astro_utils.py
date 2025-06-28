from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

def calc_zodiac_asc(birth_date, birth_time, birth_place):
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="astroconnect")
    location = geolocator.geocode(birth_place or "Москва")
    if not location:
        location = geolocator.geocode("Москва")
    pos = GeoPos(location.latitude, location.longitude)

    # birth_date 'ДД.ММ.ГГГГ', birth_time 'чч:мм'
    date_parts = birth_date.split('.')
    if ':' in birth_time:
        time_parts = birth_time.split(':')
    else:
        time_parts = ['12', '00']
    dt = Datetime(
        f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}",
        f"{time_parts[0]}:{time_parts[1]}",
        '+03:00'
    )
    chart = Chart(dt, pos)
    zodiac = chart.get("SUN").sign
    asc = chart.get("ASC").sign
    return zodiac, asc
