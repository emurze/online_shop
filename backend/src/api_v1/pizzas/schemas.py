from datetime import datetime
from typing import Optional
from uuid import UUID

from shared.schemas import Schema, PydanticMoney


class PizzaCreate(Schema):
    title: str
    description: Optional[str] = None
    price: PydanticMoney
    user_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    types: list[str] = []
    sizes: list[int] = []


class PizzaPartialUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PydanticMoney] = None
    types: Optional[list[str]] = None
    sizes: Optional[list[int]] = None


class PizzaRead(Schema):
    id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PydanticMoney] = None
    sizes: Optional[list[int]] = None
    types: Optional[list[str]] = None
    user_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PizzaPageRead(Schema):
    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: list[PizzaRead]
