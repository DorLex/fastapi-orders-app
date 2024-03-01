from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.database import SessionLocal
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


def update_order_status(order_id: int, status: str):
    stmt = update(OrderModel).values(status=status).where(OrderModel.id == order_id)

    with SessionLocal() as db:
        db.execute(stmt)
        db.commit()


def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(OrderModel).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_user_orders(db: Session, user: UserModel, skip: int = 0, limit: int = 100):
    stmt = select(OrderModel).where(OrderModel.owner_id == user.id).offset(skip).limit(limit)
    return db.scalars(stmt).all()
