from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.accounts.services.auth import get_current_user, verify_token
from src.dependencies import get_db
from src.kafka_service.producer.producer import get_producer
from src.orders.models import OrderModel
from src.orders.schemas import OrderInSchema, OrderOutSchema
from src.orders.service import OrderService

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=list[OrderOutSchema])
async def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Показать все заказы"""

    orders: list[OrderModel] = OrderService(db).get_all(skip, limit)
    return orders


@router.post('/', response_model=dict[str, str])
async def add_order(
        order: OrderInSchema,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Добавить заказ"""

    db_order: OrderModel = OrderService(db).create(current_user, order)

    message = {'order_id': db_order.id}

    producer = await get_producer()
    async with producer as pd:
        await pd.send_and_wait('orders', message)

    return {'message': f'Заказ №{db_order.id} принят на обработку. (Статус: created)'}


@router.get('/my/', response_model=list[OrderOutSchema])
async def read_my_orders(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Показать заказы текущего пользователя"""

    user_orders: list[OrderModel] = OrderService(db).get_by_user(current_user, skip, limit)
    return user_orders
