from sqlalchemy import select
from sqlalchemy.orm import Session

from logger.logger import get_logger
from src.accounts.models import UserModel
from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.schemas import OrderInSchema

logger = get_logger(__name__)


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, db_user: UserModel, order: OrderInSchema) -> OrderModel:
        db_order: OrderModel = OrderModel(
            title=order.title,
            description=order.description,
            owner_id=db_user.id
        )

        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)

        return db_order

    def get_all(self, skip: int = 0, limit: int = 100):
        query = select(OrderModel).offset(skip).limit(limit)
        return self.session.scalars(query).all()

    def get_by_id(self, order_id: int) -> OrderModel:
        query = select(OrderModel).where(OrderModel.id == order_id)
        return self.session.scalar(query)

    def get_by_user(self, db_user: UserModel, skip: int = 0, limit: int = 100):
        query = select(OrderModel).where(OrderModel.owner_id == db_user.id).offset(skip).limit(limit)
        return self.session.scalars(query).all()

    def update_status(self, db_order: OrderModel, status: OrderStatusEnum) -> OrderModel:
        if not isinstance(status, OrderStatusEnum):
            raise ValueError('Недопустимый статус заказа')

        db_order.status = status
        self.session.commit()

        logger.info(f'Статус заказа №{db_order.id} изменен на {status.value}')

        return db_order
