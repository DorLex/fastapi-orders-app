from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from logger.logger import get_logger
from src.accounts.models import UserModel
from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.schemas import OrderCreateSchema

logger = get_logger(__name__)


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, db_user: UserModel, order: OrderCreateSchema) -> OrderModel:
        db_order: OrderModel = OrderModel(
            title=order.title,
            description=order.description,
            owner_id=db_user.id
        )

        self.session.add(db_order)

        await self.session.flush()
        await self.session.commit()

        return db_order

    async def get_all(self, skip: int = 0, limit: int = 100):
        query = select(OrderModel).offset(skip).limit(limit)
        result = await self.session.scalars(query)
        return result.all()

    async def get_by_id(self, order_id: int) -> OrderModel:
        query = select(OrderModel).where(OrderModel.id == order_id)
        return await self.session.scalar(query)

    async def get_by_user(self, db_user: UserModel, skip: int = 0, limit: int = 100):
        query = select(OrderModel).where(OrderModel.owner_id == db_user.id).offset(skip).limit(limit)
        result = await self.session.scalars(query)
        return result.all()

    async def update_status(self, db_order: OrderModel, status: OrderStatusEnum) -> OrderModel:
        if not isinstance(status, OrderStatusEnum):
            raise ValueError('Недопустимый статус заказа')

        db_order.status = status
        await self.session.commit()

        logger.info(f'Статус заказа №{db_order.id} изменен на {status.value}')

        return db_order
