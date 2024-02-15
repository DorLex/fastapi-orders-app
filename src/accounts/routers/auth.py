from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.accounts.service.auth import authenticate_user, create_access_token
from src.accounts.schemas.token import Token
from src.dependencies import get_db

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token/')
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        # form_data: Annotated[UserCreate, Body()],
        db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token = create_access_token(user.username)

    return Token(access_token=access_token, token_type='bearer')
