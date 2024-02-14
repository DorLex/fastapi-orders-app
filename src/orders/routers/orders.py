from typing import Annotated

from fastapi import APIRouter, Query

from src.orders.schemas import Order

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.get('/')
async def get_orders(q: Annotated[str, Query(pattern='[0-9]')]):
    # return [{'order': 1}, {'order': 2}]

    return {'q': q}


@router.post('/')
async def add_order(order: Order) -> Order:
    return order
