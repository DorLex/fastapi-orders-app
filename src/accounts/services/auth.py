from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.accounts.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.accounts.exceptions import InvalidTokenException, CredentialsException
from src.accounts.models import UserModel
from src.accounts.schemas.token import TokenDataSchema
from src.accounts.schemas.user import UserInDBSchema
from src.accounts.services.crud import get_user_by_username
from src.accounts.services.user import UserService
from src.accounts.utils.auth import verify_password, generate_token_expire
from src.accounts.dependencies import oauth2_scheme
from src.dependencies import get_db


def create_access_token(username: str):
    token_expire = generate_token_expire(ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {'username': username, 'exp': token_expire}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str) -> UserModel | bool:
    db_user: UserModel = UserService(db).get_by_username(username)
    if not db_user:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        if username is None:
            raise InvalidTokenException

        token_data = TokenDataSchema(username=username)

    except JWTError:
        raise InvalidTokenException

    return token_data


def get_current_user(token_data: TokenDataSchema = Depends(verify_token), db: Session = Depends(get_db)) -> UserModel:
    db_user: UserModel = UserService(db).get_by_username(token_data.username)
    if db_user is None:
        raise CredentialsException
    return db_user
