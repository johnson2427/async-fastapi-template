import uvicorn
from aredis_om import Migrator
from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.postgres.session import SessionLocal, engine
from app.db.mongo.session import connect_to_mongo, close_mongo_connection


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router, prefix=settings.API_V1_STR)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    await init_db(SessionLocal())


@app.on_event("startup")
async def on_startup() -> None:
    await create_db_and_tables()
    await Migrator().run()


if __name__ == "__main__":
    uvicorn.run("app.api.api_v1.api:app", host="0.0.0.0", port=8015, reload=True)
