from fastapi import APIRouter, Depends
from starlette import status

from src.accounts.models import UserModel
from src.accounts.services.auth import get_current_user, verify_token
from src.kafka_service.producer.producer import get_producer
from src.orders.dependencies import get_order_service
from src.orders.models import OrderModel
from src.orders.schemas import OrderCreateSchema, OrderOutSchema
from src.orders.service import OrderService

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=list[OrderOutSchema])
async def read_orders(skip: int = 0, limit: int = 100, order_service: OrderService = Depends(get_order_service)):
    """Показать все заказы"""

    orders: list[OrderModel] = await order_service.get_all(skip, limit)
    return orders


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=dict[str, int | str])
async def add_order(
        order: OrderCreateSchema,
        order_service: OrderService = Depends(get_order_service),
        current_user: UserModel = Depends(get_current_user)
):
    """Добавить заказ"""

    db_order: OrderModel = await order_service.create(current_user, order)

    message = {'order_id': db_order.id, 'customer_email': current_user.email}

    producer = await get_producer()
    async with producer as pd:
        await pd.send_and_wait('orders', message)

    return {'order_id': db_order.id, 'message': f'Заказ №{db_order.id} принят на обработку. (Статус: created)'}


@router.get('/my/', response_model=list[OrderOutSchema])
async def read_my_orders(
        skip: int = 0,
        limit: int = 100,
        order_service: OrderService = Depends(get_order_service),
        current_user: UserModel = Depends(get_current_user)
):
    """Показать заказы текущего пользователя"""

    user_orders: list[OrderModel] = await order_service.get_by_user(current_user, skip, limit)
    return user_orders
