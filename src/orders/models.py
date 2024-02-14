from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base

# class Order(Base):
#     __tablename__ = 'orders'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(100))
#
#     # status = ['в обработке', 'завершен']
#
#     owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
#     owner: Mapped['User'] = relationship(back_populates='orders')
#
#     def __repr__(self) -> str:
#         return f'Order(id={self.id!r}, title={self.title!r})'
