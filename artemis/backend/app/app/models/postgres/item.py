from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.postgres.user import User


class ItemBase(SQLModel):
    title: str = Field(index=True)
    description: str = Field(index=True)


class Item(ItemBase, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="items")
