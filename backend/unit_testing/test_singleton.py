from asyncio import run

from backend.api.routes.weather.current_util import get_weather_info
from backend.src.weather_info.singleton import WeatherReportSingleton


def test_WeatherReportSingleton():
    res1 = run(get_weather_info(city="London"))
    run(WeatherReportSingleton().get_weather_info(city="London"))
    res2 = WeatherReportSingleton.report
    assert res1 == res2
    res1 = run(get_weather_info(city="Kyiv"))
    run(WeatherReportSingleton().get_weather_info(city="Kyiv"))
    res2 = WeatherReportSingleton.report
    assert res1 == res2
