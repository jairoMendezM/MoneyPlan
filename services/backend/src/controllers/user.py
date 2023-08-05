from ..models.user import User, UserDB
from ..crud.user import *

from ..utils.config import settings

from ..auth.security import (
    authenticate_user,
    get_current_active_user)

from ..auth.security import (
    create_access_token,
    verify_password_regex,
    get_hashed_password
    )

from fastapi import APIRouter, Request, HTTPException, status, Response
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from jose import jwt


user_router = APIRouter()

@user_router.post("/register/", summary="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(request: Request, user_data: UserDB) -> User:
    new_user = jsonable_encoder(user_data)
    user = getUser(request.app.database, new_user['user_name'])
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User already exist')

    # Check if user already exists
    # users = getAllUsersList(request.app.database, {"_id": 0, "user_name": 1})
    # users = get_items(users, 'user_name')
    # print("USERS", users)
    # if new_user['user_name'] in users:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User with this user name already exist"
    #     )

    # check password requirements
    if not verify_password_regex(new_user['password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User password does not meet the requirements")

    new_user['password'] = get_hashed_password(new_user['password'])
    insertUser(request.app.database, new_user)
    return new_user

@user_router.post("/login", summary="Create access and refresh tokens for user")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(request=request, user_name=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=settings.access_token_expires_in)
    access_token = create_access_token(data={'sub': user['user_name']}, expires_delta=access_token_expires)

    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )

    return response

@user_router.get("/all", summary="Get all active users")
async def get_users(request: Request, current_user: User = Depends(get_current_active_user)):
    users = getAllUsersList(request.app.database, {"_id": 0, "user_name": 0})
    return users

@user_router.get("/me/", summary="Get current user information", response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@user_router.get("/{user_name}/", summary="Get user information", response_model=UserDB)
async def get_user(request: Request, user_name: str, current_user: User = Depends(get_current_active_user)):
    if (user := getUser(request.app.database, user_name)) is not None:
        return user
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find user {user_name}")

@user_router.put("/update/", response_model=UserDB)
async def put_user(request: Request, user_data: UserDB, current_user: User = Depends(get_current_active_user)):
    updated_user = jsonable_encoder(user_data)
    user_name = updated_user['user_name']
    if (user := getUser(request.app.database, user_name)) is not None:
        user["name"] = updated_user["name"]
        user["user_name"] = updated_user["user_name"]

        # check password requirements
        if not verify_password_regex(updated_user["password"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User password does not meet the requirements")

        updated_user["password"] = get_hashed_password(updated_user["password"])

        updated_user = updateUser(request.app.database, user_name, updated_user)

        return updated_user
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not update user {user_name}")

# @user_router.delete("/user/{user_name}")
# async def delete_user(request: Request, user_name: str, User = Depends(get_current_active_user)):
