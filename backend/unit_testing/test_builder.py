import pytest
from asyncio import run

from backend.api.routes.weather.current_util import get_weather_info
from backend.src.weather_info.builder import ReportDirector, LightReportBuilder, ExtendedReportBuilder, CompleteReportBuilder


def test_LightReportBuilder():
    director = ReportDirector()
    director.set_builder(LightReportBuilder)
    res_1 = run(director.create_report("Kyiv"))
    res_2 = run(get_weather_info("Kyiv"))

    assert res_1['sky'] == res_2['weather'][0]['main']
    assert res_1['wind_speed'] == res_2['wind']['speed']
    assert res_1['temp'] == res_2['main']['temp']
    assert res_1['feels_like'] == res_2['main']['feels_like']


def test_ExtendedReportBuilder():
    director = ReportDirector()
    director.set_builder(ExtendedReportBuilder)
    res_1 = run(director.create_report("Kyiv"))
    res_2 = run(get_weather_info("Kyiv"))

    assert res_1['sky'] == res_2['weather'][0]['main']
    assert res_1['wind'] == res_2['wind']


def test_CompleteReportBuilder():
    director = ReportDirector()
    director.set_builder(CompleteReportBuilder)
    res_1 = run(director.create_report("Kyiv"))
    res_2 = run(get_weather_info("Kyiv"))

    assert res_1['coord'] == res_2['coord']
    assert res_1['weather'] == res_2['weather']
    assert res_1['main'] == res_2['main']
    assert res_1['visibility'] == res_2['visibility']
    assert res_1['wind'] == res_2['wind']
    assert res_1['clouds'] == res_2['clouds']
