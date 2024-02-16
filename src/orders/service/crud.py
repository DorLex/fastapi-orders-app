from sqlalchemy import select
from sqlalchemy.orm import Session

from src.accounts.models import User
from src.orders.models import Order
from src.orders.schemas import OrderIn


def create_order(db: Session, user: User, order: OrderIn):
    db_order = Order(
        title=order.title,
        description=order.description,
        owner_id=user.id
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(Order).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_user_orders(db: Session, user: User, skip: int = 0, limit: int = 100):
    stmt = select(Order).where(Order.owner_id == user.id).offset(skip).limit(limit)
    return db.scalars(stmt).all()
