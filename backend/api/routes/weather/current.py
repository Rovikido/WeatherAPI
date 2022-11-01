import httpx
from fastapi import APIRouter, HTTPException, Path
from beanie import PydanticObjectId

from backend.api.routes.utils import build_weather_query
from backend.db.crud import *
from backend.src.weather_info.builder import ReportDirector, LightReportBuilder, CompleteReportBuilder, \
    ExtendedReportBuilder

current_router = APIRouter(include_in_schema=True)

CURRENT_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

builder_list = {'light': LightReportBuilder, 'extended': ExtendedReportBuilder, 'complete': CompleteReportBuilder}


@current_router.get("/current/")
async def get_compiled_weather_info(city: str, report_type: str = 'light', imperial: bool = False):
    """Returns current weather info from OpenWeather's weather API.

    Args:
        city (str): Name of a city as collected by argparse
        report_type (str): One of the report types.  'light': for minimal information, 'extended' for more info, 'complete' for all available info
        imperial (bool): Use or not imperial units for temperature (Make sure to type True or False with capital letter)

    Returns:
        weather_info (dict~json): current weather info in specified city.
    """
    report_type = report_type.lower()
    if not report_type in builder_list:
        raise HTTPException(400, "Invalid report type!")
    director = ReportDirector()
    director.set_builder(builder_list[report_type])
    weather_info = await director.create_report(city, imperial)
    return weather_info


@current_router.post("/current", response_model=WeatherSchema)
async def create_weather_report(report: WeatherSchema):
    """Created a new weather report"""
    weather_report = await get_by_city(city=report.city)
    if weather_report is not None:
        raise HTTPException(409, "The forecast already exists")
    weather_report = await create(report=report)
    return weather_report


@current_router.get("/current/{city}", response_model=WeatherSchema)
async def get_weather_by_city(city: str):
    weather_report = await get_by_city(city=city)
    if weather_report is None:
        raise HTTPException(404, "The forecast for current city is not found")
    return weather_report


@current_router.get("/current/all/", response_model=List[WeatherSchema])
async def get_all_reports():
    weather_reports = await get_all()
    if weather_reports is None:
        raise HTTPException(404, "Database is empty")
    return weather_reports


@current_router.put("/current/", response_model=WeatherSchema)
async def update_report(report: WeatherSchema):
    weather_report = await update(report=report)
    if weather_report is None:
        raise HTTPException(404, "There was an error updating the weather report.")
    return weather_report
