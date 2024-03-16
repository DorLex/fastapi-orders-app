from sqlalchemy import select
from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.schemas import OrderInSchema


def create_order(db: Session, user: UserModel, order: OrderInSchema) -> OrderModel:
    db_order = OrderModel(
        title=order.title,
        description=order.description,
        owner_id=user.id
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def get_order_by_id(db: Session, order_id: int) -> OrderModel:
    stmt = select(OrderModel).where(OrderModel.id == order_id)
    return db.scalar(stmt)


def update_order_status(db: Session, db_order: OrderModel, status: OrderStatusEnum):
    if not isinstance(status, OrderStatusEnum):
        raise ValueError('Неверный статус заказа')

    db_order.status = status
    db.commit()

    return db_order


def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(OrderModel).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_user_orders(db: Session, user: UserModel, skip: int = 0, limit: int = 100):
    stmt = select(OrderModel).where(OrderModel.owner_id == user.id).offset(skip).limit(limit)
    return db.scalars(stmt).all()
