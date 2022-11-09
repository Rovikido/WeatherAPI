from asyncio import run

from backend.api.routes.weather.current_util import get_weather_info
from builder import ReportDirector, CompleteReportBuilder
from singleton import WeatherReportSingleton


# res = asyncio.run(get_weather_info(city="Kyiv"))
async def main():
    try:
        director = ReportDirector()
        director.set_builder(CompleteReportBuilder)
        res = await director.create_report("Kyiv")
        print(res)
        res = await get_weather_info(city="Kyiv")
        print(res)
        res = await WeatherReportSingleton().get_weather_info(city="Kyiv")
        print(res)
        res = await WeatherReportSingleton().get_weather_info(city="London")
        print(res)
    except ValueError as e:
        print(f'ERROR! {e}')


if __name__ == '__main__':
    run(main())