from time import sleep

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.accounts.service.auth import get_current_user, verify_token
from src.dependencies import get_db
from src.orders.schemas import OrderInSchema, OrderOutSchema
from src.orders.service.crud import create_order, get_all_orders, get_user_orders

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=list[OrderOutSchema])
async def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Показать все заказы"""

    orders = get_all_orders(db, skip=skip, limit=limit)
    return orders


def order_processing(order):
    print(f'Начало обработки заказа {order.title}')
    sleep(5)

    order.status = ''

    print(f'Заказ {order.title} обработан')


@router.post('/', response_model=dict)
async def add_order(
        order: OrderInSchema,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Добавить заказ"""

    order = create_order(db, current_user, order)

    background_tasks.add_task(order_processing, order=order)

    return {'message': f'Заказ {order.title} принят на обработку'}


@router.get('/my/', response_model=list[OrderOutSchema])
async def read_my_orders(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Показать заказы текущего пользователя"""

    user_orders = get_user_orders(db, current_user, skip=skip, limit=limit)
    return user_orders


def my_background_task(message: str):
    print(f'Начало выполнения "{message}"')
    sleep(5)
    print(f'Завершена "{message}"')


@router.post('/test-background-tasks', response_model=dict)
async def test_background_tasks(background_tasks: BackgroundTasks):
    background_tasks.add_task(my_background_task, message='Фоновая задача 1')
    return {'message': 'test'}
