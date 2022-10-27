from fastapi import FastAPI

from beanie import init_beanie

from backend.api.routes import router as main_router
from backend.db.database import client
from backend.models.current_weather import __beanie_models__


def app_factory():
	"""Application factory."""
	app = FastAPI(title='weather app')
	app.include_router(main_router)
	return app


app = app_factory()


@app.on_event("startup")
async def startup_db_client():
	await init_beanie(
		database=client.db_name, document_models=__beanie_models__
	)


@app.on_event("shutdown")
async def shutdown_db_client():
	await client.close()
