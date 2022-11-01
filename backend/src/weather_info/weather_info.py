from backend.api.routes.weather.current import get_weather_info
from asyncio import run
from builder import ReportDirector, LightReportBuilder, ExtendedReportBuilder, CompleteReportBuilder


# result = asyncio.run(get_weather_info(city="Kyiv"))
if __name__ == '__main__':
    try:
        director = ReportDirector()
        director.set_builder(LightReportBuilder())
        res = run(director.create_report("Kyiv"))
        print(res)
    except ValueError as e:
        print(f'ERROR! {e}')

