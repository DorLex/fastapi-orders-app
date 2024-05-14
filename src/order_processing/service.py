from asyncio import sleep

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from logger.logger import get_logger
from src.notifications.schemas import EmailSchema
from src.notifications.services.email_build import EmailBuildService
from src.notifications.services.email_notification import EmailNotificationService
from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.service import OrderService

logger = get_logger(__name__)


class OrderProcessingService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._order_service = OrderService(self._session)
        self._notification_service = EmailNotificationService()
        self._email_build_service = EmailBuildService()

    async def execute_order(self, order_id: int, customer_email: EmailStr) -> None:
        db_order: OrderModel = await self._order_service.get_by_id(order_id)

        try:
            if not db_order:
                await self.order_not_found(order_id, customer_email)

            await self._order_service.update_status(db_order, OrderStatusEnum.in_processing)
            await self._session.commit()

            order_processing_successful = await self.do_something_with_order(db_order)

            if not order_processing_successful:
                await self.order_processing_failed(db_order)

            await self._order_service.update_status(db_order, OrderStatusEnum.completed)
            await self._session.commit()

        except Exception as ex:
            logger.error(ex)

    async def order_not_found(self, order_id: int, customer_email: EmailStr) -> None:
        email: EmailSchema = self._email_build_service.build_order_not_found_email(order_id, customer_email)
        await self._notification_service.send_email(email)
        raise Exception(f'Заказ №{order_id} не найден!')

    async def order_processing_failed(self, db_order: OrderModel) -> None:
        email: EmailSchema = self._email_build_service.build_order_error_email(db_order)
        await self._notification_service.send_email(email)
        await self._order_service.update_status(db_order, OrderStatusEnum.failed)
        raise Exception(f'Произошла ошибка при обработке заказа №{db_order.id}!')

    async def do_something_with_order(self, _):
        await sleep(10)
        return True
