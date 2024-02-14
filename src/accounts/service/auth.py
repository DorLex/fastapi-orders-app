from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status

from src.accounts.config import SECRET_KEY, ALGORITHM
from src.accounts.schemas.token import TokenData
from src.accounts.schemas.user import UserInDB
from src.accounts.service.db import get_user_from_db
from src.accounts.utils.auth import verify_password
from src.database import fake_users_db
from src.accounts.dependencies import oauth2_scheme


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(fake_db, username: str, password: str):
    user: UserInDB = get_user_from_db(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
