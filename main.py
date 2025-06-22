from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

def generate_natal_chart(date: str, time: str, location: str = 'Moscow'):
    """Возвращает знак Солнца и Асцендента на момент рождения"""
    from datetime import datetime
    from geopy.geocoders import Nominatim

    # Преобразование строки времени
    dt = datetime.strptime(f"{date} {time}", "%d.%m.%Y %H:%M")

    # Геопозиция по умолчанию
    geo = GeoPos('55.7558', '37.6176')  # Москва

    # Геокодинг, если указан город
    if location and location.lower() != 'moscow':
        try:
            geolocator = Nominatim(user_agent="astro_bot")
            loc = geolocator.geocode(location)
            if loc:
                geo = GeoPos(str(loc.latitude), str(loc.longitude))
        except:
            pass  # если геокодинг не сработал, оставим Москву

    date_obj = Datetime(dt.strftime('%Y/%m/%d'), dt.strftime('%H:%M'), '+03:00')
    chart = Chart(date_obj, geo)

    sun_sign = chart.get('SUN').sign
    asc_sign = chart.get('ASC').sign

    return sun_sign, asc_sign
