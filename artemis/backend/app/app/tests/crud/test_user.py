import pytest
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession

from app import schemas
from app.core.security import verify_password
from app.crud.postgres.user import user_crud
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = await user_crud.create(db_session, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


@pytest.mark.asyncio
async def test_authenticate_user(db_session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = await user_crud.create(db_session, obj_in=user_in)
    authenticated_user = await user_crud.authenticate(
        db_session, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email


@pytest.mark.asyncio
async def test_not_authenticate_user(db_session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user = await user_crud.authenticate(db_session, email=email, password=password)
    assert user is None


@pytest.mark.asyncio
async def test_check_if_user_is_active(db_session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = await user_crud.create(db_session, obj_in=user_in)
    is_active = user_crud.is_active(user)
    assert is_active is True


@pytest.mark.asyncio
async def test_check_if_user_is_active_inactive(db_session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password, disabled=True)
    user = await user_crud.create(db_session, obj_in=user_in)
    is_active = user_crud.is_active(user)
    assert is_active


@pytest.mark.asyncio
async def test_check_if_user_is_superuser(db_session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password, is_superuser=True)
    user = await user_crud.create(db_session, obj_in=user_in)
    is_superuser = user_crud.is_superuser(user)
    assert is_superuser is True


@pytest.mark.asyncio
async def test_check_if_user_is_superuser_normal_user(db_session: AsyncSession) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=username, password=password)
    user = await user_crud.create(db_session, obj_in=user_in)
    is_superuser = user_crud.is_superuser(user)
    assert is_superuser is False


@pytest.mark.asyncio
async def test_get_user(db_session: AsyncSession) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = schemas.UserCreate(email=username, password=password, is_superuser=True)
    user = await user_crud.create(db_session, obj_in=user_in)
    user_2 = await user_crud.get(db_session, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = schemas.UserCreate(email=email, password=password, is_superuser=True)
    user = await user_crud.create(db_session, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = schemas.UserUpdate(password=new_password, is_superuser=True)
    await user_crud.update(db_session, db_obj=user, obj_in=user_in_update)
    user_2 = await user_crud.get(db_session, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
