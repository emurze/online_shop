from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.orders.models import Order, OrderItem


async def add_order(session: AsyncSession, order_items: list[OrderItem]):
    order = Order(order_items=order_items)
    session.add(order)
    await session.commit()
