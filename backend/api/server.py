from fastapi import FastAPI

from backend.api.routes.weather import router as weather_router


def app_factory():
	"""Application factory."""
	app = FastAPI(title='weather app')
	app.include_router(weather_router)
	return app


app = app_factory()
