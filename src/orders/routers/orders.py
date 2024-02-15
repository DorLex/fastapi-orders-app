from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.accounts.models import User
from src.accounts.service.auth import get_current_user
from src.dependencies import get_db
from src.orders.schemas import OrderIn, OrderOut
from src.orders.service.crud import create_order, get_orders

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.get('/', response_model=list[OrderOut])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = get_orders(db, skip=skip, limit=limit)
    return orders


@router.post('/')
async def add_order(
        order: OrderIn,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)
) -> OrderOut:
    return create_order(db, current_user.id, order)
