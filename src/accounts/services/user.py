from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.accounts.repositories.user import UserRepository
from src.accounts.schemas import UserCreateSchema


class UserService:

    def __init__(self, session: Session):
        self._repository = UserRepository(session)

    def create(self, user: UserCreateSchema):
        return self._repository.create(user)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        return self._repository.get_all(skip, limit)

    def get_filter_by(self, **filters):
        return self._repository.get_filter_by(**filters)

    def get_by_username(self, username: str) -> UserModel:
        return self._repository.get_by_username(username)

    def get_by_id(self, user_id: int) -> UserModel:
        return self._repository.get_by_id(user_id)
