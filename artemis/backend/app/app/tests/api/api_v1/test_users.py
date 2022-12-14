from typing import Dict

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app import schemas
from app.core.config import settings
from app.crud.postgres.user import user_crud
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_get_users_superuser_me(
    client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = await client.get(
        f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.asyncio
async def test_get_users_normal_user_me(
    client: AsyncClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = await client.get(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


@pytest.mark.skip(reason="Email is not active yet")
@pytest.mark.asyncio
async def test_create_user_new_email(
    client: AsyncClient, superuser_token_headers: dict, db_session: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = await user_crud.get_by_email(db_session, email=username)
    assert user
    assert user.email == created_user["email"]


@pytest.mark.asyncio
async def test_get_existing_user(
    client: AsyncClient, superuser_token_headers: dict, db_session: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=username, password=password)
    user = await user_crud.create(db_session, obj_in=user_in)
    user_id = user.id
    r = await client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = await user_crud.get_by_email(db_session, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


@pytest.mark.asyncio
async def test_create_user_existing_username(
    client: AsyncClient, superuser_token_headers: dict, db_session: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=username, password=password)
    await user_crud.create(db_session, obj_in=user_in)
    data = {"email": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


@pytest.mark.asyncio
async def test_create_user_by_normal_user(
    client: AsyncClient, normal_user_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_retrieve_users(
    client: AsyncClient, superuser_token_headers: dict, db_session: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=username, password=password)
    await user_crud.create(db_session, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = schemas.UserCreate(email=username2, password=password2)
    await user_crud.create(db_session, obj_in=user_in2)

    r = await client.get(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers
    )
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
