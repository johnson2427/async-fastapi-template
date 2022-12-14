from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app import schemas
from app.crud.postgres.item import item_crud
from app.models.postgres.item import Item
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_item(
    *, db_session: AsyncSession, owner_id: Optional[int] = None
) -> Item:
    if owner_id is None:
        user = await create_random_user(db_session)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    item_in = schemas.ItemCreate(title=title, description=description, id=id)
    return await item_crud.create_with_owner(
        db=db_session, obj_in=item_in, owner_id=owner_id  # type: ignore
    )
