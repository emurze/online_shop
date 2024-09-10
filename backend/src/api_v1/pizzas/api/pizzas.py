import uuid
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.pizzas import services
from api_v1.pizzas.api.categories import category_router
from api_v1.pizzas.api.sizes import size_router
from api_v1.pizzas.api.types import type_router
from api_v1.pizzas.exceptions import (
    PizzaNotFoundException,
    PizzaCategoryNotFoundException,
    PizzaUserNotFoundException,
)
from api_v1.pizzas.schemas import (
    PizzaPageRead,
    PizzaRead,
    PizzaPartialUpdate,
    PizzaCreate,
)
from shared.db import get_session
from shared.schemas import ErrorSchema

router = APIRouter(prefix="/pizzas", tags=["pizzas"])
router.include_router(size_router)
router.include_router(type_router)
router.include_router(category_router)


async def get_pizza_or_404(
    session: AsyncSession,
    pizza_id: UUID,
    for_update: bool = False,
):
    try:
        return await services.get_pizza_by_id(
            session=session,
            pizza_id=pizza_id,
            for_update=for_update,
        )
    except PizzaNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza not found",
        )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PizzaPageRead,
)
async def get_pizzas(
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = Query(
        None,
        alias="sort_by",
        description="Format: price:desc, name:asc",
    ),
    filter_by: Optional[str] = Query(
        None,
        alias="filter_by",
        description="Format: title=pizza, description=best pizza",
    ),
    session: AsyncSession = Depends(get_session),
):
    return await services.get_pizzas(
        session,
        page=page,
        limit=limit,
        sort_by=sort_by,
        filter_by=filter_by,
    )


@router.get(
    "/latest",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        }
    },
)
async def get_latest_pizza(db_session: AsyncSession = Depends(get_session)):
    try:
        return await services.get_latest_pizza(db_session)
    except PizzaNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza not found",
        )


@router.get(
    "/{pizza_id}",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        }
    },
)
async def get_pizza_by_id(
    pizza_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await get_pizza_or_404(session, pizza_id)


@router.post(
    "/{pizza_id}/sizes",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
)
async def add_size_to_pizza(
    pizza_id: UUID,
    size: int = Body(),
    session: AsyncSession = Depends(get_session),
):
    await services.add_size_to_pizza(pizza_id, size, session)
    return await services.get_pizza_by_id(session, pizza_id)


@router.delete(
    "/{pizza_id}/types",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
)
async def delete_size_from_pizza(
    pizza_id: UUID,
    type: int = Body(),  # noqa
    session: AsyncSession = Depends(get_session),
):
    pass


@router.post(
    "/{pizza_id}/types",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
)
async def add_type_to_pizza(
    pizza_id: UUID,
    type: int = Body(),  # noqa
    session: AsyncSession = Depends(get_session),
):
    pass


@router.delete(
    "/{pizza_id}/types",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
)
async def delete_type_from_pizza(
    pizza_id: UUID,
    type: int = Body(),  # noqa
    session: AsyncSession = Depends(get_session),
):
    pass


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        },
    },
)
async def create_pizza(
    pizza_dto: PizzaCreate,
    db_session: AsyncSession = Depends(get_session),
):
    try:
        pizza_id = uuid.uuid4()
        await services.add_pizza(db_session, pizza_id, pizza_dto)
        return await services.get_pizza_by_id(db_session, pizza_id)

    except PizzaUserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    except PizzaCategoryNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )


@router.patch(
    "/{pizza_id}",
    status_code=status.HTTP_200_OK,
    response_model=PizzaRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
        }
    },
)
async def update_pizza(
    pizza_id: UUID,
    pizza_dto: PizzaPartialUpdate,
    session: AsyncSession = Depends(get_session),
):
    pizza = await get_pizza_or_404(session, pizza_id, for_update=True)
    await services.update_pizza(session, pizza=pizza, pizza_dto=pizza_dto)
    await session.refresh(pizza)
    return pizza


@router.delete(
    "/{pizza_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_pizza(
    pizza_id: UUID,
    db_session: AsyncSession = Depends(get_session),
):
    await services.delete_pizza(db_session, pizza_id)
