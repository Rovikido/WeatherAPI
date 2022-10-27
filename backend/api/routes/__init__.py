from fastapi import APIRouter
from backend.api.routes.weather.current import current_router
from backend.api.routes.weather.forecast import forecast_router
from backend.api.routes.weather.air_pollution import pollution_router


router = APIRouter()


router.include_router(current_router, prefix="", tags=["current_weather"])
router.include_router(forecast_router, prefix="", tags=["weather_forecast"])
router.include_router(pollution_router, prefix="", tags=["air_pollution"])
