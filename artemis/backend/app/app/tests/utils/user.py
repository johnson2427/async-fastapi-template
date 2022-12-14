from typing import Dict

from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.crud.postgres.user import user_crud
from app.models.postgres.user import User
from app.schemas import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


async def user_authentication_headers(
    *, client: AsyncClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_random_user(db_session: AsyncSession) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = await user_crud.create(db=db_session, obj_in=user_in)
    return user


async def authentication_token_from_email(
    *, client: AsyncClient, email: str, db_session: AsyncSession
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = await user_crud.get_by_email(db_session, email=email)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = await user_crud.create(db_session, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = await user_crud.update(db_session, db_obj=user, obj_in=user_in_update)

    return await user_authentication_headers(
        client=client, email=email, password=password
    )
