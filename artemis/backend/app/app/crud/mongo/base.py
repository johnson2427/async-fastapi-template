from bson import ObjectId
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A Mongo model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, coll: AsyncIOMotorCollection, id: str) -> Optional[Any]:
        if (db_obj := await coll.find_one({"_id": ObjectId(id)})) is not None:
            return db_obj  # type: ignore
        return None

    async def get_multi(
            self, coll: AsyncIOMotorCollection, *, skip: int = 0, limit: int = 100
    ) -> List[Any]:
        cursor = coll.find()
        return await cursor.to_list(length=limit)

    async def create(
        self, coll: AsyncIOMotorCollection, *, obj_in: CreateSchemaType
    ) -> ModelType:
        await coll.insert_one(jsonable_encoder(obj_in))
        return obj_in

    async def update(
        self,
        coll: AsyncIOMotorCollection,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field in list(db_obj.dict().keys()):
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        _id = db_obj.id
        delattr(db_obj, "id")
        await coll.update_one(
            {"_id": _id},
            {"$set": jsonable_encoder(db_obj)}
        )
        setattr(db_obj, "id", _id)
        return db_obj

    async def remove(self, coll: AsyncIOMotorCollection, *, id: int) -> ModelType:
        q = await coll.find_one({"_id": id})
        if q:
            await coll.delete_one({"_id": id})
        return q
