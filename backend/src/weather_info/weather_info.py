from backend.api.routes.weather.current_util import get_weather_info
from asyncio import run
from builder import ReportDirector, LightReportBuilder, ExtendedReportBuilder, CompleteReportBuilder


# result = asyncio.run(get_weather_info(city="Kyiv"))
async def main():
    try:
        director = ReportDirector()
        director.set_builder(LightReportBuilder)
        res = await director.create_report("Kyiv")
        print(res)
    except ValueError as e:
        print(f'ERROR! {e}')


if __name__ == '__main__':
    run(main())