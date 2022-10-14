from urllib.parse import urlencode
import requests
from fastapi import APIRouter

from backend.config import WEATHER_API_KEY

router = APIRouter(include_in_schema=True)

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


def build_weather_query(city: str, imperial=False) -> str:
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        city (str): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    units = "imperial" if imperial else "metric"
    request_data = {'q': city,
                    'appid': WEATHER_API_KEY,
                    'units': units}
    url_values = urlencode(request_data)
    full_url = BASE_WEATHER_API_URL + '?' + url_values
    return full_url


@router.get("/weather/")
def get_weather_info(city: str, imperial=False):
    """Returns current weather info from OpenWeather's weather API.

    Args:
        city (str): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        weather_info (dict~json): current weather info in specified city.
    """
    url = build_weather_query(city=city, imperial=imperial)
    response = requests.get(url)
    weather_info = response.json()
    return weather_info


@router.get("/")
def index():
    """Just an index method:)"""
    return "Weather app"
