from backend.api.routes.weather import get_weather_info


result = get_weather_info(city="Kyiv")
print(result)
