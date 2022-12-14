from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    full_name: Optional[str] = Field(nullable=True)
    email: str = Field(index=True, nullable=False, sa_column_kwargs={"unique": True})
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    items: List["Item"] = Relationship(  # type: ignore # noqa: F821
        back_populates="owner"
    )
