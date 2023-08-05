from pymongo import database as Database
from fastapi import HTTPException
from ..models.auth import Status

def getUser(database: Database, user_name: str):
    return database.user.find_one({'user_name': user_name})

def getAllUsersList(database: Database, filter: dict):
    return list(database.user.find({}, filter))

def insertUser(databse: Database, new_user: dict):
    return databse.user.insert_one(new_user)

def updateUser(database: Database, user_name: str, updated_user: dict):
    del updated_user['_id']
    return database.user.find_one_and_replace({"user_name": user_name}, updated_user)

def deleteUser(database: Database, user_name:str):
    if (user := database.user.find_one({'user_name': user_name})) is not None:
        deleted = database.user.drop({'user_name': {user_name}})
        if not deleted:
            raise HTTPException(status_code=404, detail=f"User {user_name} not found")
        return Status(message=f"Deleted user {user_name}")
    raise HTTPException(status_code=403, detail=f"Not authorized to delete")