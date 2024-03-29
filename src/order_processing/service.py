from asyncio import sleep

from sqlalchemy.orm import Session

from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.service import OrderService


class OrderProcessingService:

    def __init__(self, session: Session):
        self._order_service = OrderService(session)

    async def execute_order(self, order_id):
        db_order: OrderModel = self._order_service.get_by_id(order_id)

        await self._order_service.update_status(db_order, OrderStatusEnum.in_processing)

        order_processing_successful = await self.do_something_with_order(db_order)

        await self._order_service.update_status(db_order, OrderStatusEnum.completed)

    async def do_something_with_order(self, _):
        await sleep(10)
        return True
