from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.repositories.user import UserRepository
from src.accounts.services.user import UserService
from src.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token/')


async def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
