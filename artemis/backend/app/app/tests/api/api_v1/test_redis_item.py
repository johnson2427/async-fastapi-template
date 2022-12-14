from typing import Any, Dict

import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_create_redis_item(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any]
) -> None:
    data = {"name": "hello"}
    response = await client.post(
        url=f"{settings.API_V1_STR}/redis_item/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]


@pytest.mark.asyncio
async def test_delete_redis_item(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any]
) -> None:
    response = await client.get(
        url=f"{settings.API_V1_STR}/redis_item/",
        headers=superuser_token_headers,
    )
    content = response.json()
    response = await client.delete(
        url=f"{settings.API_V1_STR}/redis_item/",
        headers=superuser_token_headers,
        params={"pk": content["pk"]},
    )
    assert response.status_code == 200
    assert response.json() == 1


@pytest.mark.asyncio
async def test_get_items(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any]
) -> None:
    response = await client.get(
        url=f"{settings.API_V1_STR}/redis_item/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content["name"], dict)
