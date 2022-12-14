import asyncio
from typing import AsyncGenerator, Callable, Dict, Generator

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.mongo.session import mongo_client
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:  # type: ignore
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator:
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
    async with engine.begin() as connection:
        async_session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with async_session() as sess:
            yield sess
            await sess.flush()
            await sess.rollback()


@pytest_asyncio.fixture
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db() -> AsyncGenerator:
        yield db_session

    return _override_get_db


@pytest_asyncio.fixture
def app(override_get_db: AsyncSession) -> FastAPI:
    from app.api.deps import get_db
    from app.main import app

    app.dependency_overrides[get_db] = override_get_db

    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as c:
        yield c


@pytest_asyncio.fixture
def mongo_db() -> Generator:
    yield mongo_client


@pytest_asyncio.fixture
async def superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest_asyncio.fixture
async def normal_user_token_headers(
    client: AsyncClient, db_session: AsyncSession
) -> Dict[str, str]:
    return await authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db_session=db_session
    )
