from sqlalchemy import select
from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.accounts.schemas import UserCreateSchema
from src.accounts.utils.auth import get_password_hash


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: UserCreateSchema) -> UserModel:
        hashed_password = get_password_hash(user.password)

        user: UserModel = UserModel(
            username=user.username,
            hashed_password=hashed_password
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_all(self, skip: int = 0, limit: int = 100):
        query = select(UserModel).offset(skip).limit(limit)
        return self.session.scalars(query).all()

    def get_filter_by(self, **filters):
        query = select(UserModel).filter_by(**filters)
        return self.session.scalars(query).all()

    def get_by_username(self, username: str) -> UserModel:
        query = select(UserModel).where(UserModel.username == username)
        return self.session.scalar(query)

    def get_by_id(self, user_id: int) -> UserModel:
        query = select(UserModel).where(UserModel.id == user_id)
        return self.session.scalar(query)
