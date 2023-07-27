from Models.user import User, UserDB, Token, TokenData


from utils.user_utils import (oath2_scheme)
from utils.user_utils import (
    create_access_token,
    verify_password,
    verify_password_regex,
    get_hashed_password,
    get_items
    )

from profiles.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from profiles.database_connection import USER_COLLECTION



from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from jose import jwt


#====================================================================================================================
#====================================================================================================================
def authenticate_user(request: Request, user_name: str, password: str):
    user = request.app.database[USER_COLLECTION].find_one({'user_name': user_name})
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
            token, SECRET_KEY, algorithms=ALGORITHM)
        user_name: str = payload.get("sub")
        token_data = TokenData(user_name=user_name)
    except jwt.JWTError:
        raise credential_exception

    user = request.app.database[USER_COLLECTION].find_one({'user_name': token_data.user_name})

    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(request: Request, current_user: UserDB = Depends(get_current_user)):
    if current_user['disabled']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
#====================================================================================================================
#====================================================================================================================

user_router = APIRouter()

@user_router.post("/user/sign_up/", response_description="Create a new user", status_code=status.HTTP_201_CREATED)
async def user_signUp(request: Request, user_data: UserDB):
    new_user = jsonable_encoder(user_data)

    # Check if user already exists
    users = get_items(list(request.app.database[USER_COLLECTION].find({}, {"_id": 0, "user_name": 1})), 'user_name')
    if new_user['user_name'] in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this user name already exist"
        )

    # check password requirements
    if not verify_password_regex(new_user['password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User password does not meet the requirements")

    new_user['password'] = get_hashed_password(new_user['password'])
    request.app.database[USER_COLLECTION].insert_one(new_user)

    return new_user

@user_router.post("/user/login", summary="Create access and refresh tokens for user", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(request=request, user_name=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user['user_name']}, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}

@user_router.get("/user/all")
async def get_users(request: Request, User = Depends(get_current_active_user)):
    users = list(request.app.database[USER_COLLECTION].find({}, {"_id": 0, "password": 0}))
    return users

@user_router.get("/user/me/", response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@user_router.get("/user/{user_name}/", response_model=UserDB)
async def get_item(request: Request, user_name: str, User = Depends(get_current_active_user)):
    if (user := request.app.database[USER_COLLECTION].find_one({'user_name': user_name})) is not None:
        return user
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find user {user_name}")


@user_router.put("/user/update/")
async def put_user(request: Request,user_data:  UserDB,current_user: UserDB = Depends(get_current_active_user)):
    updated_user = jsonable_encoder(user_data)
    user_name = updated_user['user_name']
    if (user := request.app.database[USER_COLLECTION].find_one({'user_name': user_name})) is not None:
        user["name"] = updated_user["name"]
        user["user_name"] = updated_user["user_name"]
        user["password"] = get_hashed_password(updated_user["password"])
        updated_user = request.app.database[USER_COLLECTION].find_one_and_replace({"user_name": user["user_name"]}, updated_user)
        return updated_user
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not update user {updated_user['user_name']}")
