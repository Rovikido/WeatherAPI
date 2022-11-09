# This script is used only for testing

import httpx

from backend.api.routes.utils import build_weather_query

CURRENT_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


async def get_weather_info(city: str, imperial=False):
    """Returns current weather info from OpenWeather's weather API.

    Args:
        city (str): Name of a city as collected by argparse
        imperial (bool): Use or not imperial units for temperature (Make sure to type True or False with capital letter)

    Returns:
        weather_info (dict~json): current weather info in specified city.
    """
    url = build_weather_query(base_url=CURRENT_WEATHER_API_URL, city=city, imperial=imperial)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        weather_info = response.json()
    return weather_info
