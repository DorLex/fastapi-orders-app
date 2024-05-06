from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.accounts.models import UserModel
from src.accounts.services.auth import authenticate_user, create_access_token
from src.accounts.schemas.token import TokenSchema
from src.dependencies import get_db

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token/', response_model=TokenSchema)
async def login_by_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_db)
):
    """Авторизация"""

    user: UserModel = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token = create_access_token(user.username)

    return TokenSchema(access_token=access_token, token_type='bearer')
