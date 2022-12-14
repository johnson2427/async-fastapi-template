import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app import schemas
from app.crud.postgres.item import item_crud
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


@pytest.mark.asyncio
async def test_create_item(db_session: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = schemas.ItemCreate(title=title, description=description)
    user = await create_random_user(db_session)
    item = await item_crud.create_with_owner(
        db=db_session, obj_in=item_in, owner_id=user.id  # type: ignore
    )
    assert item.title == title
    assert item.description == description
    assert item.owner_id == user.id


@pytest.mark.asyncio
async def test_get_item(db_session: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = schemas.ItemCreate(title=title, description=description)
    user = await create_random_user(db_session)
    item = await item_crud.create_with_owner(
        db=db_session, obj_in=item_in, owner_id=user.id  # type: ignore
    )
    stored_item = await item_crud.get(db=db_session, id=item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.description == stored_item.description
    assert item.owner_id == stored_item.owner_id


@pytest.mark.asyncio
async def test_update_item(db_session: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = schemas.ItemCreate(title=title, description=description)
    user = await create_random_user(db_session)
    item = await item_crud.create_with_owner(
        db=db_session, obj_in=item_in, owner_id=user.id  # type: ignore
    )
    description2 = random_lower_string()
    item_update = schemas.ItemUpdate(description=description2)
    item2 = await item_crud.update(db=db_session, db_obj=item, obj_in=item_update)
    assert item.id == item2.id
    assert item.title == item2.title
    assert item2.description == description2
    assert item.owner_id == item2.owner_id


@pytest.mark.asyncio
async def test_delete_item(db_session: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = schemas.ItemCreate(title=title, description=description)
    user = await create_random_user(db_session)
    item = await item_crud.create_with_owner(
        db=db_session, obj_in=item_in, owner_id=user.id  # type: ignore
    )
    item2 = await item_crud.remove(db=db_session, id=item.id)  # type: ignore
    item3 = await item_crud.get(db=db_session, id=item.id)
    assert item3 is None
    assert item2.id == item.id
    assert item2.title == title
    assert item2.description == description
    assert item2.owner_id == user.id
