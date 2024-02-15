from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))

    hashed_password: Mapped[str] = mapped_column(String)

    orders: Mapped[list['Order']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r})'
