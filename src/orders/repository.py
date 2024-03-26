from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.database import SessionLocal
from src.orders.models import OrderModel


class OrderRepository:
    session: sessionmaker = SessionLocal

    def get_all(self, skip: int = 0, limit: int = 100):
        with self.session() as db:
            query = select(OrderModel).offset(skip).limit(limit)
            return db.scalars(query).all()
