from src.notifications.schemas import EmailSchema
from src.orders.models import OrderModel


class EmailBuildService:
    def build_email(self, emails: list, subject: str, message: str) -> EmailSchema:
        email = EmailSchema(
            emails=emails,
            subject=subject,
            message=message
        )

        return email

    def build_order_status_changed_email(self, order: OrderModel) -> EmailSchema:
        email = EmailSchema(
            emails=[order.owner.email],
            subject='Статус заказа изменен',
            message=f'Статус Вашего заказа №{order.id} изменен на "{order.status.value}"'
        )

        return email
