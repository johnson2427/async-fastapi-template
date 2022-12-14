from typing import Any, List, Optional

from aredis_om import NotFoundError
from fastapi import APIRouter, HTTPException

from app.models.redis.item import Item
from app.schemas.redis.item import ItemCreate

router = APIRouter()


@router.get("/", response_model=List[Item])
async def list_redis_items(name: Optional[str] = None) -> Any:
    items = []
    pks = [pk async for pk in await Item.all_pks()]
    for pk in pks:
        item = await Item.get(pk)
        if name is None:
            items.append(item)
        else:
            if item.name == name:
                items.append(item)
    return items


@router.post("/", response_model=Item)
async def post_redis_item(item: ItemCreate) -> Any:
    return await Item(name=item.name).save()


@router.get("/{pk}", response_model=Item)
async def get_redis_item(pk: str) -> Any:
    pks = [val async for val in await Item.all_pks()]
    for val in pks:
        item = await Item.get(val)
        if item.pk == pk:
            return item

    raise HTTPException(status_code=404, detail=f"Item {id} not found")


@router.put("/{id}", response_model=Item)
async def update_redis_item(pk: str, patch: Item) -> Any:
    try:
        item = await Item.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Item {pk} not found")
    item.name = patch.name
    return await item.save()


@router.delete("/{pk}")
async def delete_redis_item(pk: str) -> int:
    """
    Deletes a Redis Item

    Args:
        pk (str): Redis pk value for the `Item`

    Returns:
        int: Redis id of the `Item` deleted
    """

    try:
        return await Item.delete(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Item {pk} not found")
