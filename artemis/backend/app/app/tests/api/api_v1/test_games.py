import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.tests.utils.item import create_random_item


@pytest.mark.asyncio
async def test_create_game(client: AsyncClient, superuser_token_headers: dict) -> None:
    data = {
        "date": "10-12-2920",
        "games": {
            "0": {
                "schedule": {"away": "CHC", "home": "CWS"},
                "score": {"away": 10, "home": 8}
            }
        }
    }
    response = await client.post(
        f"{settings.API_V1_STR}/games/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["games"] == data["games"]
    assert content["date"] == data["date"]
    assert content["id"]


@pytest.mark.asyncio
async def test_read_game(
    client: AsyncClient, superuser_token_headers: dict, db_session: AsyncSession
) -> None:
    game = await create_random_item(db_session=db_session)
    response = await client.get(
        f"{settings.API_V1_STR}/games/{game.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["games"] == game.games
    assert content["date"] == game.date
    assert content["_id"] == game.id


@pytest.mark.asyncio
async def test_read_games(
    client: AsyncClient, superuser_token_headers: dict, db_session: AsyncSession
) -> None:
    game = await create_random_item(db_session=db_session)
    response = await client.get(
        f"{settings.API_V1_STR}/games/?skip=0&limit=100",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
