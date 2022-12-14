from typing import List

from fastapi.encoders import jsonable_encoder
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app import schemas
from app.crud.postgres.base import CRUDBase
from app.models.postgres.item import Item


class CRUDItem(CRUDBase[Item, schemas.ItemCreate, schemas.ItemUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: schemas.ItemCreate, owner_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        q = await db.exec(  # type: ignore
            select(self.model)  # type: ignore
            .where(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return q.all()


item_crud = CRUDItem(Item)
