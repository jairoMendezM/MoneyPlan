from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

import re

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from ..utils.config import settings
from ..crud.user import getUser
from ..models.auth import TokenData
from ..models.user import UserDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login", scheme_name="JWT")

def verify_password_regex(password) -> bool:
    return re.search(r'[A-Za-z0-9@#$%^&+=\-\_]{8,}', password)

def verify_password(password, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)

def get_hashed_password(password) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.access_token_expires_in)

    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)
    return encoded_jwt

def get_items(dict_list, key):
    items = []
    for item in dict_list:
        items.append(item[key])

    return items

def authenticate_user(request: Request, user_name: str, password: str):
    user = getUser(request.app.database, user_name)
    if user is not None:
        if not verify_password(password, user['password']):
            return False
        return user
    return False

async def get_current_user(request: Request, token: str = Depends(oath2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm)
        user_name: str = payload.get("sub")
        token_data = TokenData(user_name=user_name)
    except jwt.JWTError:
        raise credential_exception

    user = getUser(request.app.database, token_data.user_name)

    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(request: Request, current_user: UserDB = Depends(get_current_user)):
    if current_user['disabled']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user