from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.accounts.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.accounts.exceptions import InvalidTokenException, CredentialsException
from src.accounts.schemas.token import TokenData
from src.accounts.schemas.user import UserInDB
from src.accounts.service.crud import get_user_by_username
from src.accounts.utils.auth import verify_password, generate_token_expire
from src.accounts.dependencies import oauth2_scheme
from src.dependencies import get_db


def create_access_token(username: str):
    token_expire = generate_token_expire(ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {'username': username, 'exp': token_expire}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str):
    user: UserInDB = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        if username is None:
            raise InvalidTokenException

        token_data = TokenData(username=username)

    except JWTError:
        raise InvalidTokenException

    return token_data


def get_current_user(token_data: TokenData = Depends(verify_token), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise CredentialsException
    return user
