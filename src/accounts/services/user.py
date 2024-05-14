from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.accounts.models import UserModel
from src.accounts.repositories.user import UserRepository
from src.accounts.schemas import UserCreateSchema


class UserService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = UserRepository(self._session)

    async def registration(self, user: UserCreateSchema):
        check_user_registered = await self.get_filter_by(username=user.username, email=user.email)

        if check_user_registered:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Пользователь с таким именем и почтой уже зарегистрирован'
            )

        db_user: UserModel = await self._repository.create(user)

        return db_user

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        return await self._repository.get_all(skip, limit)

    async def get_filter_by(self, **filters) -> list[UserModel]:
        return await self._repository.get_filter_by(**filters)

    async def get_by_username(self, username: str) -> UserModel:
        return await self._repository.get_by_username(username)

    async def get_by_id(self, user_id: int) -> UserModel:
        return await self._repository.get_by_id(user_id)
