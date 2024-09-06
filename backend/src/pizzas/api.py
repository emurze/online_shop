from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from pizzas.models import Pizza
from pizzas.schemas import PizzaRead, PizzaCreate, PizzaUpdate
from shared.db import get_session
from shared.schemas import ErrorSchema

router = APIRouter(prefix="/pizzas", tags=["pizzas"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PizzaRead],
)
async def get_pizzas(db_session: AsyncSession = Depends(get_session)):
    query = select(Pizza)
    result = await db_session.execute(query)
    return result.scalars()


@router.get(
    "/{pizzas_id}/",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Pizza not found",
            "model": ErrorSchema,
        }
    },
)
async def get_pizza_by_id(
    pizzas_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    query = select(Pizza).filter_by(id=pizzas_id)
    pizza = (await db_session.execute(query)).scalar_one_or_none()

    if pizza is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return pizza


@router.get(
    "/latest/",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Last pizza not found",
            "model": ErrorSchema,
        }
    },
)
async def get_latest_pizza(db_session: AsyncSession = Depends(get_session)):
    query = select(Pizza).order_by(Pizza.title).limit(1)
    last_pizza = (await db_session.execute(query)).scalar_one_or_none()

    if last_pizza is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return last_pizza


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PizzaRead,
)
async def create_pizza(
    pizza: PizzaCreate,
    db_session: AsyncSession = Depends(get_session),
):
    pizza = Pizza(title=pizza.title)
    db_session.add(pizza)
    await db_session.commit()
    return PizzaRead.model_validate(pizza)


@router.delete("/{pizza_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pizza(
    pizza_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    command = delete(Pizza).filter_by(id=pizza_id)
    await db_session.execute(command)
    await db_session.commit()


@router.put(
    "/{pizza_id}/",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Pizza created",
            "model": PizzaRead,
        }
    },
)
async def update_pizza(
    pizza_id: int,
    pizza_dto: PizzaUpdate,
    db_session: AsyncSession = Depends(get_session),
):
    # todo: add correct typing
    pizza: Any = await db_session.get(Pizza, pizza_id, with_for_update=True)

    if pizza is None:
        pizza = Pizza(id=pizza_id, title=pizza_dto.title)
        db_session.add(pizza)
    else:
        pizza.update(title=pizza_dto.title)

    await db_session.commit()
    return PizzaRead.model_validate(pizza)  # todo: different codes


# async def get_user_or_404(
#     user_id: str,
#     user_manager: BaseUserManager = Depends(get_user_manager),
# ) -> NoReturn:
#     try:
#         parsed_id = user_manager.parse_id(user_id)
#         return await user_manager.get(parsed_id)
#     except (UserNotExists, InvalidID) as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
#

# @router.get(
#     "/",
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {
#             "description": "Missing token or inactive user"
#         },
#         status.HTTP_403_FORBIDDEN: {  # custom permissions
#             "description": "Not a superuser.",
#         },
#         status.HTTP_404_NOT_FOUND: {"The user does not exist."},
#     },
# )
# async def get_pizza(user: User = Depends(get_user_or_404)):
#     print(user)
