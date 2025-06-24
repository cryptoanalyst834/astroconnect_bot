from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib import const

def generate_astrology_data(date: str, time: str, lat: float, lon: float):
    """
    Генерация натальной карты на основе даты, времени и координат.
    Возвращает знак Солнца и Асцендент.
    """
    try:
        datetime = Datetime(f'{date}', f'{time}', '+03:00')  # Можно сменить offset
        pos = GeoPos(str(lat), str(lon))
        chart = Chart(datetime, pos, IDs=const.LIST_OBJECTS)

        sun_sign = chart.get(const.SUN).sign
        asc_sign = chart.get(const.ASC).sign

        return {
            'sun_sign': sun_sign,
            'asc_sign': asc_sign
        }
    except Exception as e:
        return {'error': str(e)}
