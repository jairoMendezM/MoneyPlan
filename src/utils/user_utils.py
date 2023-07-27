from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

import re

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from profiles.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

from profiles.database_connection import USER_COLLECTION

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
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def get_items(dict_list, key):
    items = []
    for item in dict_list:
        items.append(item[key])

    return items