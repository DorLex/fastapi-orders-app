from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.orders.enums import OrderStatusEnum


class OrderModel(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(
        ENUM(OrderStatusEnum),
        default=OrderStatusEnum.in_processing
    )

    description: Mapped[str] = mapped_column(String)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped['UserModel'] = relationship(back_populates='orders')

    def __repr__(self) -> str:
        return f'Order(id={self.id!r}, title={self.title!r})'
