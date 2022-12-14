from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import schemas
from app.api.deps import get_current_active_user, get_db
from app.crud.postgres.item import item_crud
from app.crud.postgres.user import user_crud
from app.models.postgres.item import Item
from app.models.postgres.user import User

router = APIRouter()


@router.get("/", response_model=List[Item])
async def read_items(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """

    Args:
        db (`sqlmodel.ext.asyncio.session.AsyncSession`):
        skip (int):
        limit (int):
        current_user (:class:`~models.postgres.user.User`):

    Returns:
        Any
    """
    if user_crud.is_superuser(current_user):
        items = await item_crud.get_multi(db, skip=skip, limit=limit)
    else:
        items = await item_crud.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit  # type: ignore
        )
    return items


@router.post("/", response_model=Item)
async def create_item(
    *,
    db: AsyncSession = Depends(get_db),
    item_in: schemas.ItemCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = await item_crud.create_with_owner(
        db=db, obj_in=item_in, owner_id=current_user.id  # type: ignore
    )
    return item


@router.put("/{id}", response_model=Item)
async def update_item(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    item_in: schemas.ItemUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = await item_crud.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not user_crud.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = await item_crud.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=Item)
async def read_item(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = await item_crud.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not user_crud.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.delete("/{id}", response_model=Item)
async def delete_item(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = await item_crud.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not user_crud.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = await item_crud.remove(db=db, id=id)
    return item
