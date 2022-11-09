"""Holds building methods for displaying weather data and forecasts."""

from abc import ABCMeta, abstractmethod

from backend.src.weather_info.singleton import WeatherReportSingleton


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
        self._city = ''
        self._res_report = {}
        self.reset()

    def reset(self):
        """Prepares builder for next report"""
        self._res_report.clear()
        self._res_report['city'] = ''

    def report(self):
        """Returns report"""
        res = self._res_report.copy()
        self.reset()
        return res

    def set_city(self, city: str, imperial=False):
        self._city = city
        self._res_report['city'] = city

    def add_coord(self):
        pass

    def add_sky(self):
        self._res_report['sky'] = WeatherReportSingleton.report['weather'][0]['main']

    def add_wind(self):
        self._res_report['wind_speed'] = WeatherReportSingleton.report['wind']['speed']

    def add_temperature(self):
        self._res_report['temp'] = WeatherReportSingleton.report['main']['temp']
        self._res_report['feels_like'] = WeatherReportSingleton.report['main']['feels_like']

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
        self.reset()

    def reset(self):
        """Prepares builder for next report"""
        self._res_report.clear()
        self._res_report['city'] = ''

    def report(self):
        """Returns report"""
        res = self._res_report.copy()
        self.reset()
        return res

    def set_city(self, city: str, imperial=False):
        self._city = city
        self._res_report['city'] = city

    def add_coord(self):
        self._res_report['coord'] = WeatherReportSingleton.report['coord']

    def add_sky(self):
        self._res_report['sky'] = WeatherReportSingleton.report['weather'][0]['main']

    def add_wind(self):
        self._res_report['wind'] = WeatherReportSingleton.report['wind']

    def add_temperature(self):
        self._res_report['temp'] = WeatherReportSingleton.report['main']['temp']
        self._res_report['feels_like'] = WeatherReportSingleton.report['main']['feels_like']

    def add_visibility(self):
        self._res_report['visibility'] = WeatherReportSingleton.report['visibility']

    def add_humidity(self):
        self._res_report['humidity'] = WeatherReportSingleton.report['main']['humidity']

    def add_everything(self):
        pass


class CompleteReportBuilder(WeatherReportBuilder):
    """Almost complete report configuration(without system info)"""
    def __init__(self):
        self._res_report = {}
        self.reset()

    def reset(self):
        """Prepares builder for next report"""
        self._res_report.clear()
        self._res_report['city'] = ''

    def report(self):
        """Returns report"""
        res = self._res_report.copy()
        self.reset()
        return res

    def set_city(self, city: str, imperial=False):
        self._city = city
        self._res_report['city'] = city

    def add_everything(self):
        self._res_report['coord'] = WeatherReportSingleton.report['coord']
        self._res_report['weather'] = WeatherReportSingleton.report['weather']
        self._res_report['main'] = WeatherReportSingleton.report['main']
        self._res_report['visibility'] = WeatherReportSingleton.report['visibility']
        self._res_report['wind'] = WeatherReportSingleton.report['wind']
        self._res_report['clouds'] = WeatherReportSingleton.report['clouds']

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

    def set_builder(self, builder):
        self._builder = builder()

    async def create_report(self, city: str, imperial=False):
        """Used to initiate report creation
        Args:
            imperial: use imperial unitc or not
            city (str): Name of the city for query search
        """

        if self._builder is None:
            raise ValueError("Builder does not exist")
        self._builder.set_city(city, imperial)
        await WeatherReportSingleton().get_weather_info(city, imperial)
        self._builder.add_everything()
        self._builder.add_coord()
        self._builder.add_sky()
        self._builder.add_wind()
        self._builder.add_temperature()
        self._builder.add_visibility()
        self._builder.add_humidity()

        return self._builder.report()
