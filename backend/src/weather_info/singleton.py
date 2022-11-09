from threading import Lock

import httpx

from backend.api.routes.utils import build_weather_query


class WeatherReportSingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


# class WeatherSchemeSingleton(metaclass=WeatherSchemeSingletonMeta):
#     scheme: WeatherSchema = None
#     report: WeatherReport = None
#
#     async def create(self, report: WeatherSchema) -> WeatherSchema:
#         self.report = WeatherReport(**report.dict())
#         print(report.dict())
#         await self.report.insert()
#         return self.report

class WeatherReportSingleton(metaclass=WeatherReportSingletonMeta):
    report = {}
    city: str = None
    imperial: bool = None
    CURRENT_WEATHER_API_URL = None

    def __init__(self, url="http://api.openweathermap.org/data/2.5/weather"):
        WeatherReportSingleton.CURRENT_WEATHER_API_URL = url

    @staticmethod
    def change_properties(city: str, imperial: bool = False):
        WeatherReportSingleton.city = city
        WeatherReportSingleton.imperial = imperial
        WeatherReportSingleton.report.clear()

    @staticmethod
    async def get_weather_info(city: str, imperial=False):
        """Returns current weather info from OpenWeather's weather API.

        Args:
            city (str): Name of a city as collected by argparse
            imperial (bool): Use or not imperial units for temperature (Make sure to type True or False with capital letter)

        Returns:
            weather_info (dict~json): current weather info in specified city.
        """
        WeatherReportSingleton.change_properties(city, imperial)

        url = build_weather_query(base_url=WeatherReportSingleton.CURRENT_WEATHER_API_URL,
                                  city=WeatherReportSingleton.city, imperial=WeatherReportSingleton.imperial)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            weather_info = response.json()
        WeatherReportSingleton.report = weather_info
        return weather_info
