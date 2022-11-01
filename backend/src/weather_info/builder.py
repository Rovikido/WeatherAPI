"""Holds building methods for displaying weather data and forecasts."""

from abc import ABCMeta, abstractmethod
from backend.api.routes.weather.current import get_weather_info
import asyncio


class WeatherReportBuilder(metaclass=ABCMeta):
    """Template for builders"""

    @abstractmethod
    def set_city(self, city: str):
        pass

    @abstractmethod
    def add_everything(self):
        pass

    @abstractmethod
    def add_sky(self):
        """IS ASYNC"""
        pass

    @abstractmethod
    def add_wind(self):
        pass

    @abstractmethod
    def add_temperature(self):
        pass

    @abstractmethod
    def add_visibility(self):
        pass

    @abstractmethod
    def add_coord(self):
        pass

    @abstractmethod
    def add_humidity(self):
        pass


class LightReportBuilder(WeatherReportBuilder):
    """Minimal report configuration"""
    def __init__(self):
        self._res_report = {}
        self._initial_report = {}
        self.reset()

    def reset(self):
        """Prepares builder for next report"""
        self._city = ''
        self._res_report.clear()
        self._initial_report.clear()
        self._res_report['city'] = ''

    def report(self):
        """Returns report"""
        res = self._res_report.copy()
        self.reset()
        return res

    async def set_city(self, city: str):
        self._city = city
        self._res_report['city'] = city
        report = await get_weather_info(city=city)
        self._initial_report = report

    def add_coord(self):
        pass

    def add_sky(self):
        self._res_report['sky'] = self._initial_report['weather'][0]['main']

    def add_wind(self):
        self._res_report['wind_speed'] = self._initial_report['wind']['speed']

    def add_temperature(self):
        self._res_report['temp'] = self._initial_report['main']['temp']
        self._res_report['feels_like'] = self._initial_report['main']['feels_like']

    def add_visibility(self):
        pass

    def add_humidity(self):
        pass

    def add_everything(self):
        pass


class ExtendedReportBuilder(WeatherReportBuilder):
    """Extended report configuration"""
    def __init__(self):
        self._res_report = {}
        self._initial_report = {}
        self.reset()

    def reset(self):
        """Prepares builder for next report"""
        self._city = None
        self._res_report = {}
        self._initial_report = {}

    def report(self):
        """Returns report"""
        res = self._res_report.copy()
        self.reset()
        return res

    async def set_city(self, city: str):
        self._city = city
        self._res_report['city'] = city
        report = await get_weather_info(city=city)
        self._initial_report = report

    def add_coord(self):
        self._res_report['coord'] = self._initial_report['coord']

    def add_sky(self):
        self._res_report['sky'] = self._initial_report['weather'][0]['main']

    def add_wind(self):
        self._res_report['wind'] = self._initial_report['wind']

    def add_temperature(self):
        self._res_report['temp'] = self._initial_report['main']['temp']
        self._res_report['feels_like'] = self._initial_report['main']['feels_like']

    def add_visibility(self):
        self._res_report['visibility'] = self._initial_report['visibility']

    def add_humidity(self):
        self._res_report['humidity'] = self._initial_report['main']['humidity']

    def add_everything(self):
        pass


class CompleteReportBuilder(WeatherReportBuilder):
    """Almost complete report configuration(without system info)"""
    def __init__(self):
        self._res_report = {}
        self._initial_report = {}
        self.reset()

    def reset(self):
        """Prepares builder for next report"""
        self._city = ''
        self._res_report.clear()
        self._initial_report.clear()
        self._res_report['city'] = ''

    def report(self):
        """Returns report"""
        res = self._res_report.copy()
        self.reset()
        return res

    async def set_city(self, city: str):
        self._city = city
        self._res_report['city'] = city
        report = await get_weather_info(city=city)
        self._initial_report = report

    def add_everything(self):
        self._res_report['coord'] = self._initial_report['coord']
        self._res_report['weather'] = self._initial_report['weather']
        self._res_report['main'] = self._initial_report['main']
        self._res_report['visibility'] = self._initial_report['visibility']
        self._res_report['wind'] = self._initial_report['wind']
        self._res_report['clouds'] = self._initial_report['clouds']

    def add_coord(self):
        pass

    def add_sky(self):
        pass

    def add_wind(self):
        pass

    def add_temperature(self):
        pass

    def add_visibility(self):
        pass

    def add_humidity(self):
        pass


class ReportDirector:
    """Manages specific builders"""
    def __init__(self):
        self._builder = None

    def set_builder(self, builder: WeatherReportBuilder):
        self._builder = builder

    async def create_report(self, city: str):
        """Used to initiate report creation
        Args:
            city (str): Name of the city for query search
        """
        if self._builder is None:
            raise ValueError("Builder does not exist")
        await self._builder.set_city(city)

        self._builder.add_everything()
        self._builder.add_coord()
        self._builder.add_sky()
        self._builder.add_wind()
        self._builder.add_temperature()
        self._builder.add_visibility()
        self._builder.add_humidity()

        return self._builder.report()


