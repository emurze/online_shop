from pydantic import EmailStr

from api_v1.pizzas.schemas import PizzaRead
from shared.schemas import Schema


class UserRead(Schema):
    username: str
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool
    pizzas: list[PizzaRead] = []
