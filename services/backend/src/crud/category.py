import uuid
from pymongo import database as Database
from fastapi import Depends, HTTPException, status

from ..models.category import Category
from ..models.auth import Status

def createCategory(database: Database, category: Category):
    return database.category.insert_one(category)

def getCategory(database: Database, name: str):
    return database.category.find_one({'name': name})

def getAllCategories(database: Database):
    return list(database.category.find({}, {'_id': 0}))

def getSubCategories(database: Database, name: str):
    return dict(database.category.find_one({'name': name}, {"_id":0, "subcategories": 1}))


def addSubCategory(database: Database, name: str, subcategory: str):
    category = database.category.find_one({'name': name})
    if category:
        if subcategory in category['subcategories']:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Subcategory {subcategory} already exists in category {category}")
        category['subcategories'].append(subcategory)
        database.category.update_one({'name': name}, {'$set': {'subcategories': category['subcategories']}})
        return Status(message=f"Subcategory {subcategory} added to category {name}")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find category {name}")

def deleteSubCategory(database: Database, name: str, subcategory: str):
    category = database.category.find_one({'name': name})
    if category:
        try:
            category['subcategories'].remove(subcategory)
            category = database.category.update_one({'name': name}, {'$set': {'subcategories': category['subcategories']}})
            return Status(message=f"Subcategory {subcategory} removed from category {name}")
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete subcategory {subcategory}. Subcategory does not exist for category {name}.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not update category {name}")

def deleteCategory(database: Database, name: str):
    if (database.category.find_one({'name': name})) is not None:
        deleted = database.category.delete_one({'name': name})
        if not deleted:
            raise HTTPException(status_code=400, detail=f"Could not delete category: {name}")
        return Status(message=f"Category {name} deleted")
    raise HTTPException(status_code=404, detail=f"Category {name} not found")