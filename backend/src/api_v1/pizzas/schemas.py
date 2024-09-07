from datetime import datetime
from typing import Optional
from uuid import UUID

from shared.schemas import Schema, PydanticMoney


class PizzaCreate(Schema):
    title: str
    description: Optional[str] = None
    price: PydanticMoney
    user_id: None = None


class PizzaPartialUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PydanticMoney] = None
    user_id: None = None


class PizzaRead(Schema):
    id: UUID
    title: str
    description: str
    price: PydanticMoney
    created_at: datetime
    updated_at: datetime
    user_id: None = None
