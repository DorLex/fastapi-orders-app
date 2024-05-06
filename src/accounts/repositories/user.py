from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.models import UserModel
from src.accounts.schemas import UserCreateSchema
from src.accounts.utils.auth import get_password_hash


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreateSchema) -> UserModel:
        hashed_password = get_password_hash(user.password)

        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )

        self.session.add(db_user)

        await self.session.flush()
        await self.session.commit()

        return db_user

    async def get_all(self, skip: int = 0, limit: int = 100):
        query = select(UserModel).offset(skip).limit(limit)
        result = await self.session.scalars(query)
        return result.all()

    async def get_filter_by(self, **filters):
        query = select(UserModel).filter_by(**filters)
        result = await self.session.scalars(query)
        return result.all()

    async def get_by_username(self, username: str) -> UserModel:
        query = select(UserModel).where(UserModel.username == username)
        return await self.session.scalar(query)

    async def get_by_id(self, user_id: int) -> UserModel:
        query = select(UserModel).where(UserModel.id == user_id)
        return await self.session.scalar(query)
