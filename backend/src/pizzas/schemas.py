from datetime import datetime

from shared.schemas import Schema


class PizzaCreate(Schema):
    title: str


class PizzaUpdate(Schema):
    title: str


class PizzaRead(Schema):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
